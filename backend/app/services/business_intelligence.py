from typing import Any, Iterable, List
import re

from app.graph.state import GraphState
from app.schemas.agents import GTMStrategy, SWOTAnalysis


def _data(output: Any) -> Any:
    return getattr(output, "data", output)


def _list(value: Any) -> List[str]:
    if not value:
        return []
    if isinstance(value, list):
        return [str(item) for item in value if item]
    return [str(value)]


def _label_from_item(item: Any) -> str:
    if isinstance(item, str):
        return item.strip()
    if isinstance(item, dict):
        name = item.get("name")
        category = item.get("category")
        if name and category:
            return f"{name} ({category})"
        if name:
            return str(name).strip()
    name = getattr(item, "name", None)
    category = getattr(item, "category", None)
    if name and category:
        return f"{name} ({category})"
    if name:
        return str(name).strip()
    return str(item).strip()


def _first(items: Iterable[str], limit: int = 4) -> List[str]:
    result = []
    for item in items:
        clean = str(item).strip()
        if clean and clean not in result:
            result.append(clean)
        if len(result) >= limit:
            break
    return result


def _clean_text(value: Any) -> str:
    if value is None:
        return ""
    if hasattr(value, "model_dump"):
        value = value.model_dump()
    if isinstance(value, dict):
        for key in ("name", "title", "label", "company_name"):
            if value.get(key):
                name = str(value.get(key)).strip()
                category = str(value.get("category") or value.get("type") or "").strip()
                return f"{name} ({category})" if category else name
        return ", ".join(_clean_text(item) for item in value.values() if item)
    text = str(value).strip()
    if not text:
        return ""
    name_match = re.search(r"name=['\"]([^'\"]+)['\"]", text)
    if name_match:
        category_match = re.search(r"category=['\"]([^'\"]+)['\"]", text)
        name = name_match.group(1).strip()
        if category_match:
            return f"{name} ({category_match.group(1).strip()})"
        return name
    return text


def _competitor_name(value: Any) -> str:
    cleaned = _clean_text(value)
    if cleaned:
        return cleaned.split("(", 1)[0].strip()
    return ""


def _market_threat_text(value: Any) -> str:
    cleaned = _clean_text(value)
    if not cleaned:
        return ""
    lowered = cleaned.lower()
    if any(token in lowered for token in ["name=", "strengths=", "weaknesses="]):
        name = _competitor_name(value) or cleaned
        category = ""
        if isinstance(value, dict):
            category = str(value.get("category") or value.get("type") or "").strip()
        if hasattr(value, "model_dump"):
            dumped = value.model_dump()
            category = str(dumped.get("category") or dumped.get("type") or "").strip()
        if category:
            return f"Strong competition from {name} ({category})."
        return f"Strong competition from {name}."
    if lowered.startswith(("regulatory", "competitive", "competition", "margin", "pricing", "supply", "delivery", "retention")):
        return cleaned if cleaned.endswith(".") else f"{cleaned}."
    return cleaned if cleaned.endswith(".") else f"{cleaned}."


def _self_reference(name: str, company: str, concept: str) -> bool:
    normalized = name.strip().lower()
    reference_text = f"{company} {concept}".strip().lower()
    if not normalized:
        return False
    if normalized == company.lower() or normalized == concept.lower():
        return True
    tokens = {token for token in re.split(r"[^a-z0-9]+", reference_text) if len(token) > 2}
    return normalized in tokens


from app.services.market_context import detect_market_context, format_currency_amount


def build_swot(state: GraphState) -> SWOTAnalysis:
    scout = _data(state.get("scout_output"))
    analyst = _data(state.get("analyst_output"))
    treasury = _data(state.get("treasury_output"))
    commander = _data(state.get("commander_output"))
    idea = state.get("startup_idea")
    market_ctx = detect_market_context(idea)
    company_name = getattr(idea, "company_name", "")
    concept = getattr(idea, "business_concept", "")

    competitors = _list(getattr(analyst, "direct_competitors", [])) + _list(getattr(analyst, "indirect_competitors", []))
    competitor_names = []
    for comp in competitors:
        name = _competitor_name(comp)
        if name and not _self_reference(str(name), company_name, concept):
            competitor_names.append(str(name))

    growth_rate = getattr(scout, 'growth_rate', None)
    growth_str = f"Estimated growth rate: {growth_rate}% CAGR." if growth_rate else "Market growth requires validation."

    cac = getattr(treasury, 'estimated_cac', 0) or 0
    ltv = getattr(treasury, 'estimated_ltv', 0) or 0
    ltv_cac_str = f"Target LTV/CAC ratio of {round(ltv / max(cac, 1), 2)}x." if cac > 0 and ltv > 0 else "Unit economics requires validation."

    strengths = _first([
        *_list(getattr(commander, "success_factors", [])),
        growth_str,
        ltv_cac_str,
    ])

    weaknesses = _first([
        *_list(getattr(analyst, "feature_gaps", [])),
        f"Break-even is projected at {getattr(treasury, 'break_even_months', 'unknown')} months.",
        "Execution depends on validating acquisition and retention assumptions.",
    ])

    market_size_val = getattr(scout, 'market_size_local', None) or getattr(scout, 'market_size_usd', 0)
    market_size_fmt = format_currency_amount(market_size_val, market_ctx.currency_symbol, market_ctx.currency_code)

    opportunities = _first([
        *_list(getattr(scout, "regional_opportunities", [])),
        *_list(getattr(scout, "customer_behavior", [])),
        *_list(getattr(scout, "trends", [])),
        f"Target market opportunity in {market_ctx.country} estimated at {market_size_fmt}.",
        "Use focused positioning to enter underserved segments before broad expansion.",
    ])

    market_threats = [
        _label_from_item(item)
        for item in getattr(analyst, "market_threats", [])
        if _label_from_item(item)
    ]
    threats = _first([
        *market_threats,
        f"Competitive pressure from {', '.join(competitor_names[:3])}." if competitor_names else f"Competitive pressure from incumbents in {market_ctx.country}.",
        "Margin pressure if acquisition or operating costs rise faster than revenue.",
    ])

    return SWOTAnalysis(
        strengths=strengths,
        weaknesses=weaknesses,
        opportunities=opportunities,
        threats=threats,
    )


def build_gtm_strategy(state: GraphState) -> GTMStrategy:
    idea = state.get("startup_idea")
    market_ctx = detect_market_context(idea)
    scout = _data(state.get("scout_output"))
    analyst = _data(state.get("analyst_output"))
    treasury = _data(state.get("treasury_output"))
    commander = _data(state.get("commander_output"))

    target_users = []
    if idea and idea.target_users:
        target_users.append(idea.target_users)
    target_users.extend(_list(getattr(commander, "research_priorities", []))[:2])
    if not target_users:
        target_users = [f"Early adopters in {market_ctx.country} with urgent pain around the stated problem."]

    customer_behavior = _first([
        *_list(getattr(scout, "customer_behavior", [])),
        f"Target customer decision cycle in {market_ctx.country} driven by clear ROI and immediate utility.",
    ])

    regional_opportunities = _first([
        *_list(getattr(scout, "regional_opportunities", [])),
        f"High-priority launch regions and hubs in {market_ctx.country}.",
    ])

    positioning = (
        f"Position {idea.company_name if idea else 'the startup'} in {market_ctx.country} as a focused solution for "
        f"{idea.target_users if idea and idea.target_users else 'the target segment'}, "
        f"using {getattr(treasury, 'pricing_model', 'a validated pricing model')} aligned with local customer purchasing power."
    )

    # Adapt channels to market factors
    channel_list = [
        "Direct outreach to high-intent customer segments",
        "Partnerships with ecosystem platforms and distribution partners",
        "Founder-led proof and case studies",
        "Referral loops from pilot customer cohorts",
    ]
    if market_ctx.is_india and any("whatsapp" in f.lower() for f in market_ctx.relevant_factors):
        channel_list.insert(1, "WhatsApp-enabled customer engagement and community loops")

    channels = _first(channel_list)

    cac_val = getattr(treasury, 'estimated_cac', 0)
    cac_fmt = format_currency_amount(cac_val, market_ctx.currency_symbol, market_ctx.currency_code) if cac_val else "modeled target"

    customer_acquisition = _first([
        *_list(getattr(scout, "customer_behavior", [])),
        f"Keep CAC disciplined below the {cac_fmt} target.",
        "Prioritize narrow pilots with measurable retention and repeat usage.",
        "Convert competitor feature gaps into differentiated value messaging.",
    ])

    launch_plan = _first([
        *_list(getattr(scout, "regional_opportunities", [])),
        *_list(getattr(commander, "execution_plan", [])),
        f"Launch with a controlled {market_ctx.country} pilot, measure unit economics, then expand channel coverage.",
    ], limit=5)

    growth_strategy = _first([
        *_list(getattr(scout, "customer_behavior", [])),
        *_list(getattr(scout, "trends", [])),
        *_list(getattr(analyst, "feature_gaps", [])),
        "Expand into adjacent regional segments after core unit economics are proven.",
    ], limit=5)

    return GTMStrategy(
        target_customers=target_users[:5],
        positioning=f"{positioning} Customer behavior: {customer_behavior}. Regional opportunities: {regional_opportunities}.",
        channels=channels,
        customer_acquisition=customer_acquisition,
        launch_plan=launch_plan,
        growth_strategy=growth_strategy,
    )

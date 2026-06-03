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


def build_swot(state: GraphState) -> SWOTAnalysis:
    scout = _data(state.get("scout_output"))
    analyst = _data(state.get("analyst_output"))
    treasury = _data(state.get("treasury_output"))
    commander = _data(state.get("commander_output"))
    idea = state.get("startup_idea")
    company_name = getattr(idea, "company_name", "")
    concept = getattr(idea, "business_concept", "")

    competitors = _list(getattr(analyst, "direct_competitors", [])) + _list(getattr(analyst, "indirect_competitors", []))
    competitor_names = []
    for comp in competitors:
        name = _competitor_name(comp)
        if name and not _self_reference(str(name), company_name, concept):
            competitor_names.append(str(name))

    strengths = _first([
        *_list(getattr(commander, "success_factors", [])),
        f"Market is growing at an estimated {getattr(scout, 'growth_rate', 'unknown')}% CAGR.",
        f"Revenue model supports LTV/CAC of {round(getattr(treasury, 'estimated_ltv', 0) / max(getattr(treasury, 'estimated_cac', 1), 1), 2)}.",
    ])

    weaknesses = _first([
        *_list(getattr(analyst, "feature_gaps", [])),
        f"Break-even is projected at {getattr(treasury, 'break_even_months', 'unknown')} months.",
        "Execution depends on validating acquisition and retention assumptions.",
    ])

    opportunities = _first([
        *_list(getattr(scout, "regional_opportunities", [])),
        *_list(getattr(scout, "customer_behavior", [])),
        *_list(getattr(scout, "trends", [])),
        f"Estimated market size is ${getattr(scout, 'market_size_usd', 0):,.0f}.",
        "Use focused positioning to enter underserved segments before broad expansion.",
    ])

    market_threats = [
        _label_from_item(item)
        for item in getattr(analyst, "market_threats", [])
        if _label_from_item(item)
    ]
    threats = _first([
        *market_threats,
        f"Competitive pressure from {', '.join(competitor_names[:3])}." if competitor_names else "Competitive pressure from incumbents and substitutes.",
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
    scout = _data(state.get("scout_output"))
    analyst = _data(state.get("analyst_output"))
    treasury = _data(state.get("treasury_output"))
    commander = _data(state.get("commander_output"))

    target_users = []
    if idea and idea.target_users:
        target_users.append(idea.target_users)
    target_users.extend(_list(getattr(commander, "research_priorities", []))[:2])
    if not target_users:
        target_users = ["Early adopters with urgent pain around the stated business problem."]

    customer_behavior = _first([
        *_list(getattr(scout, "customer_behavior", [])),
        "Convenience-led, repeat-purchase behavior in dense urban catchments.",
    ])

    regional_opportunities = _first([
        *_list(getattr(scout, "regional_opportunities", [])),
        "High-density metro clusters and nearby satellite markets.",
    ])

    positioning = (
        f"Position {idea.company_name if idea else 'the startup'} as a focused solution for {idea.target_users if idea and idea.target_users else 'the target segment'}, "
        f"using {getattr(treasury, 'pricing_model', 'a validated pricing model')} and evidence from the strongest market trends."
    )

    channels = _first([
        "Direct outreach to high-intent customer segments",
        "Partnerships with category platforms and ecosystem operators",
        "Founder-led content and proof-led case studies",
        "Referral loops from successful early customers",
    ])

    customer_acquisition = _first([
        *_list(getattr(scout, "customer_behavior", [])),
        f"Keep CAC below the modeled ${getattr(treasury, 'estimated_cac', 0):,.0f} threshold.",
        "Prioritize narrow pilots with measurable retention and repeat usage.",
        "Convert competitor feature gaps into landing-page and sales objections.",
    ])

    launch_plan = _first([
        *_list(getattr(scout, "regional_opportunities", [])),
        *_list(getattr(commander, "execution_plan", [])),
        "Launch with a controlled pilot, publish proof metrics, then expand channel coverage.",
    ], limit=5)

    growth_strategy = _first([
        *_list(getattr(scout, "customer_behavior", [])),
        *_list(getattr(scout, "trends", [])),
        *_list(getattr(analyst, "feature_gaps", [])),
        "Expand into adjacent segments after unit economics are validated.",
    ], limit=5)

    return GTMStrategy(
        target_customers=target_users[:5],
        positioning=f"{positioning} Customer behavior: {customer_behavior}. Regional opportunities: {regional_opportunities}.",
        channels=channels,
        customer_acquisition=customer_acquisition,
        launch_plan=launch_plan,
        growth_strategy=growth_strategy,
    )

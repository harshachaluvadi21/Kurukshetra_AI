import json
import os
import re
from datetime import datetime
from typing import Any, Dict, List, Optional

from app.events.event_bus import event_bus
from app.events.event_types import AppEvent, EventType
from app.graph.state import GraphState
from app.reports.exporters.json_exporter import JsonExporter
from app.reports.exporters.markdown_exporter import MarkdownExporter
from app.reports.exporters.pdf_exporter import PdfExporter
from app.reports.models import CitationMapping, ExecutiveReport, ReportSection
from app.services.business_intelligence import build_gtm_strategy, build_swot
from app.services.market_context import detect_market_context, format_currency_amount, MarketContext


class ReportBuilder:
    def __init__(self):
        self.output_dir = os.path.join(os.path.dirname(__file__), "..", "..", "outputs", "reports")
        os.makedirs(self.output_dir, exist_ok=True)

    async def build(self, state: GraphState) -> GraphState:
        run_id = state.get("run_id", "unknown")
        idea = state.get("startup_idea")
        market_ctx = detect_market_context(idea)
        
        scout = self._data(state.get("scout_output"))
        analyst = self._data(state.get("analyst_output"))
        treasury = self._data(state.get("treasury_output"))
        commander = self._data(state.get("commander_output"))
        critic = self._data(state.get("critic_output"))
        swot = state.get("swot_analysis") or build_swot(state)
        gtm = state.get("gtm_strategy") or build_gtm_strategy(state)
        battle_score = state.get("battle_score")
        confidence = state.get("confidence_score")
        verdict = state.get("battle_verdict", "Unknown")
        citations = self._collect_citations(scout, analyst)
        startup_name = getattr(idea, "company_name", "the startup")

        score = battle_score.composite_score if battle_score else 0
        conf = confidence.overall_confidence if confidence else 0
        final_call = self._final_call(verdict, score, critic)
        top_strength = self._sentence(getattr(swot, "strengths", []), "Not generated")
        top_risk = self._sentence(self._get(critic, "failure_risks"), "Not generated")
        top_actions = self._bullets(
            self._items(self._get(gtm, "launch_plan"))[:2]
            + self._items(self._get(critic, "mitigation_recommendations"))[:2]
            + self._items(self._get(commander, "execution_plan"))[:2]
        )

        currency_sym = market_ctx.currency_symbol
        currency_code = market_ctx.currency_code
        country = market_ctx.country

        # Format financials with status labels
        tam_num = self._number(self._get(scout, "market_size_local") or self._get(scout, "market_size_usd"))
        tam_str = format_currency_amount(tam_num, currency_sym, currency_code) if tam_num > 0 else "Insufficient verified data; requires validation."
        tam_status = self._get(scout, "tam_status", "Estimated")

        cagr_num = self._number(self._get(scout, "growth_rate"))
        cagr_str = f"{cagr_num:.1f}%" if cagr_num > 0 else "Insufficient verified data; requires validation."

        rev_y1_num = self._number(self._get(treasury, "projected_revenue_year_1"))
        rev_y1_str = format_currency_amount(rev_y1_num, currency_sym, currency_code) if rev_y1_num > 0 else "Insufficient verified data; requires validation."

        rev_y3_num = self._number(self._get(treasury, "projected_revenue_year_3"))
        rev_y3_str = format_currency_amount(rev_y3_num, currency_sym, currency_code) if rev_y3_num > 0 else "Insufficient verified data; requires validation."

        cac_num = self._number(self._get(treasury, "estimated_cac"))
        cac_str = format_currency_amount(cac_num, currency_sym, currency_code) if cac_num > 0 else "Insufficient verified data; requires validation."

        ltv_num = self._number(self._get(treasury, "estimated_ltv"))
        ltv_str = format_currency_amount(ltv_num, currency_sym, currency_code) if ltv_num > 0 else "Insufficient verified data; requires validation."

        be_months = self._number(self._get(treasury, "break_even_months"))
        be_str = f"{be_months:.0f} months" if be_months > 0 else "Insufficient verified data; requires validation."

        ltv_cac_str = f"{ltv_num / cac_num:.2f}x" if cac_num > 0 and ltv_num > 0 else "Insufficient verified data; requires validation."

        titles = market_ctx.section_titles

        # --- SECTION 1: Executive Summary ---
        sec_1 = ReportSection(
            title=titles[1],
            content_markdown=(
                f"# {titles[1]}\n\n"
                f"**Idea:** {idea.company_name}\n\n"
                f"**Target Market:** {country} (Default Currency: {currency_code} / {currency_sym})\n\n"
                f"**Business Concept:** {idea.business_concept}\n\n"
                f"**Verdict:** {verdict}\n\n"
                f"**Battle Score:** {score}/100\n\n"
                f"**Confidence:** {conf * 100:.0f}%\n\n"
                f"**Recommendation:** {final_call}\n\n"
                f"**Top Strengths:** {top_strength}\n\n"
                f"**Top Risks:** {top_risk}\n\n"
                f"**Top Actions:**\n{top_actions}\n"
                f"**Market Timing:** {self._sentence(self._get(scout, 'trends'), 'Market timing requires pilot validation.')}\n\n"
                "> [!NOTE]\n"
                "> **Data Classification Standard**: Quantitative metrics are categorized as FACTS (user inputs), "
                "ESTIMATES (source-backed), ASSUMPTIONS (modeled benchmarks), or PROPOSED TARGETS (pilot targets). "
                "Where reliable data is absent, metrics are marked as 'Insufficient verified data; requires validation.'"
            )
        )

        # --- SECTION 2: Business Concept ---
        startup_type = self._get(commander, "startup_type", "Technology-enabled Startup")
        sec_2 = ReportSection(
            title=titles[2],
            content_markdown=(
                f"## {titles[2]}\n\n"
                f"- **Company / Product Name:** {idea.company_name} [FACT: User-provided]\n"
                f"- **Industry Classification:** {idea.industry} / {self._get(scout, 'industry', idea.industry)}\n"
                f"- **Business Model Classification:** {startup_type}\n"
                f"- **Core Business Concept:** {idea.business_concept} [FACT: User-provided]\n\n"
                f"**Strategic Thesis:**\n"
                f"{idea.company_name} addresses inefficiencies in the {idea.industry} market in {country} by delivering a "
                f"focused solution tailored to the operational realities and unit economic constraints of {country}."
            )
        )

        # --- SECTION 3: Problem & Customer ---
        prob = idea.problem_statement or "Specific problem statement not provided; inferred from concept."
        users = idea.target_users or "Target users not explicitly specified."
        ecosystem_factors = "\n".join(f"- **{f}:** Contextually integrated into workflow & customer touchpoints." for f in market_ctx.relevant_factors) if market_ctx.relevant_factors else f"- Operating within standard {country} commercial regulations."
        sec_3 = ReportSection(
            title=titles[3],
            content_markdown=(
                f"## {titles[3]}\n\n"
                f"**The Problem:** [FACT: User-provided]\n"
                f"{prob}\n\n"
                f"**Target Customer Segment:** [FACT: User-provided]\n"
                f"{users}\n\n"
                f"**Market Context & Ecosystem Factors ({country}):**\n"
                f"{ecosystem_factors}"
            )
        )

        # --- SECTION 4: India / Target Market Opportunity ---
        sec_4 = ReportSection(
            title=titles[4],
            content_markdown=(
                f"## {titles[4]}\n\n"
                f"- **Total Addressable Market (TAM):** {tam_str} [{tam_status}]\n"
                f"- **Estimated Growth Rate (CAGR):** {cagr_str} [ESTIMATE: Source-based]\n"
                f"- **Currency:** {currency_code} ({currency_sym})\n\n"
                f"**Key Macro Trends in {country}:**\n"
                f"{self._bullets(self._get(scout, 'trends'))}\n"
                f"**High-Potential Regional Opportunities & Hubs:**\n"
                f"{self._bullets(self._get(scout, 'regional_opportunities'))}"
            ),
            citations=citations
        )

        # --- SECTION 5: Customer Behavior ---
        sec_5 = ReportSection(
            title=titles[5],
            content_markdown=(
                f"## {titles[5]}\n\n"
                f"**Observed Adoption & Purchasing Behavior in {country}:**\n"
                f"{self._bullets(self._get(scout, 'customer_behavior'))}\n"
                f"**Decision Drivers:**\n"
                f"- Clear ROI and immediate utility over abstract long-term benefits.\n"
                f"- High price sensitivity and low tolerance for friction during trial/onboarding.\n"
                f"- Relies on peer recommendations, social proof, and verifiable pilot results."
            )
        )

        # --- SECTION 6: Value Proposition & USP ---
        sec_6 = ReportSection(
            title=titles[6],
            content_markdown=(
                f"## {titles[6]}\n\n"
                f"**Core Value Proposition:**\n"
                f"{gtm.positioning}\n\n"
                f"**Critical Success Factors & Moats:**\n"
                f"{self._bullets(self._get(commander, 'success_factors'))}"
            )
        )

        # --- SECTION 7: Competitor Analysis ---
        sec_7 = ReportSection(
            title=titles[7],
            content_markdown=(
                f"## {titles[7]}\n\n"
                f"**Direct Competitors in {country}:**\n"
                f"{self._competitor_bullets(self._get(analyst, 'direct_competitors'), startup_name)}\n"
                f"**Indirect & Substitute Competitors:**\n"
                f"{self._competitor_bullets(self._get(analyst, 'indirect_competitors'), startup_name)}\n"
                f"**Market Threats:**\n"
                f"{self._bullets(self._get(analyst, 'market_threats'))}"
            ),
            citations=citations
        )

        # --- SECTION 8: Feature Gaps ---
        sec_8 = ReportSection(
            title=titles[8],
            content_markdown=(
                f"## {titles[8]}\n\n"
                f"**Unaddressed Market & Feature Gaps in {country}:**\n"
                f"{self._bullets(self._get(analyst, 'feature_gaps'))}\n"
                f"**Wedge Opportunity:**\n"
                f"By closing these specific operational and service gaps, {startup_name} can capture high-intent initial cohorts without direct margin-eroding price wars."
            )
        )

        # --- SECTION 9: Business Model ---
        rev_sub = idea.revenue_model or "Not specified by user."
        sec_9 = ReportSection(
            title=titles[9],
            content_markdown=(
                f"## {titles[9]}\n\n"
                f"- **Submitted Revenue Model:** {rev_sub} [FACT: User-provided]\n"
                f"- **Recommended Operating Model:** {self._get(treasury, 'pricing_model', startup_type)} [RECOMMENDATION]\n"
                f"- **Monetization Mechanics:** Multi-stream or unit-based transactional fee structure calibrated to {country} purchasing power.\n"
                f"- **Value Chain Alignment:** Aligned to minimize upfront friction while preserving sustainable unit margins."
            )
        )

        # --- SECTION 10: Pricing Strategy ---
        sec_10 = ReportSection(
            title=titles[10],
            content_markdown=(
                f"## {titles[10]}\n\n"
                f"- **Proposed Model:** {self._get(treasury, 'pricing_model', 'Value-based tiering')} [MODEL ASSUMPTION]\n"
                f"- **Currency:** {currency_code} ({currency_sym})\n"
                f"- **Customer Purchasing Power Calibration:** Tailored to local willingness to pay in {country}.\n"
                f"- **Tiering Strategy:** Freemium/low-friction trial wedge expanding into premium recurring or transactional tiers upon demonstrated value."
            )
        )

        # --- SECTION 11: Financial & Unit Economics ---
        sec_11 = ReportSection(
            title=titles[11],
            content_markdown=(
                f"## {titles[11]}\n\n"
                f"- **Projected Year 1 Revenue:** {rev_y1_str} [MODEL ASSUMPTION]\n"
                f"- **Projected Year 3 Revenue:** {rev_y3_str} [MODEL ASSUMPTION]\n"
                f"- **Estimated CAC:** {cac_str} [PROPOSED TARGET]\n"
                f"- **Estimated LTV:** {ltv_str} [PROPOSED TARGET]\n"
                f"- **Target LTV / CAC Ratio:** {ltv_cac_str} [PROPOSED TARGET]\n"
                f"- **Projected Break-even Timeline:** {be_str} [MODEL ASSUMPTION]\n\n"
                "> [!IMPORTANT]\n"
                "> **Disclaimer on Pilot Projections**: All financial metrics above represent preliminary model assumptions "
                "and proposed target thresholds. They MUST NOT be presented or treated as historical or verified business results."
            )
        )

        # --- SECTION 12: MVP ---
        mvp_items = self._items(self._get(commander, "mvp_scope"))
        if not mvp_items:
            mvp_items = [
                f"Core functional workflow resolving primary user pain point in {country}.",
                f"Lightweight onboarding and payment integration ({currency_code}).",
                "Basic analytics dashboard to track pilot cohort activation and retention.",
            ]
        sec_12 = ReportSection(
            title=titles[12],
            content_markdown=(
                f"## {titles[12]}\n\n"
                f"**Core MVP Scope for Initial Pilot:**\n"
                f"{self._bullets(mvp_items)}\n"
                f"**Development Principle:**\n"
                f"Build the thinnest viable wedge to test customer willingness to engage and pay before investing in comprehensive platform automation."
            )
        )

        # --- SECTION 13: Validation Strategy ---
        val_items = self._items(self._get(commander, "validation_strategy"))
        if not val_items:
            val_items = [
                f"Conduct 25+ structured customer discovery interviews with target users in {country}.",
                "Launch concierge or manual pilot with 10-20 active users/businesses.",
                f"Measure organic repeat usage and willingness to pay in {currency_sym}.",
            ]
        sec_13 = ReportSection(
            title=titles[13],
            content_markdown=(
                f"## {titles[13]}\n\n"
                f"**Validation Steps Before Major Capital Allocation:**\n"
                f"{self._bullets(val_items)}\n"
                f"**Pass / Fail Criteria:**\n"
                f"- Minimum 40% user retention or positive repeat transactional behavior over 30 days.\n"
                f"- Demonstrable customer willingness to pay at or above the modeled unit economic floor."
            )
        )

        # --- SECTION 14: India / Target GTM Strategy ---
        sec_14 = ReportSection(
            title=titles[14],
            content_markdown=(
                f"## {titles[14]}\n\n"
                f"**Target Customer Cohorts:**\n"
                f"{self._bullets(gtm.target_customers)}\n\n"
                f"**Positioning Statement:**\n"
                f"{gtm.positioning}\n\n"
                f"**Primary Distribution Channels in {country}:**\n"
                f"{self._bullets(gtm.channels)}\n"
                f"**Customer Acquisition Playbook:**\n"
                f"{self._bullets(gtm.customer_acquisition)}\n"
                f"**Phased Launch Plan:**\n"
                f"{self._bullets(gtm.launch_plan)}"
            )
        )

        # --- SECTION 15: Success Metrics ---
        metrics = self._items(self._get(commander, "success_metrics"))
        if not metrics:
            metrics = [
                f"North Star: Monthly Active Users / Transacting Accounts in {country}.",
                f"Customer Acquisition Cost disciplined below {cac_str}.",
                f"Cohort 30-day retention exceeding 35%.",
                f"Positive unit contribution margin per transaction/seat.",
            ]
        sec_15 = ReportSection(
            title=titles[15],
            content_markdown=(
                f"## {titles[15]}\n\n"
                f"**Pilot & Growth KPI Targets:** [PROPOSED TARGETS]\n"
                f"{self._bullets(metrics)}\n"
                "> [!NOTE]\n"
                "> Target thresholds are established for validation guidance and must be calibrated against real pilot telemetry."
            )
        )

        # --- SECTION 16: Risks & Mitigation ---
        sec_16 = ReportSection(
            title=titles[16],
            content_markdown=(
                f"## {titles[16]}\n\n"
                f"- **Assessed Risk Level:** {self._get(critic, 'risk_level', 'Medium')} [ASSESSMENT]\n\n"
                f"**Primary Failure Risks:**\n"
                f"{self._bullets(self._get(critic, 'failure_risks'))}\n"
                f"**Mitigation Recommendations:**\n"
                f"{self._bullets(self._get(critic, 'mitigation_recommendations'))}"
            )
        )

        # --- SECTION 17: Challenged Assumptions ---
        sec_17 = ReportSection(
            title=titles[17],
            content_markdown=(
                f"## {titles[17]}\n\n"
                f"**Critical Assumptions Requiring Validation:**\n"
                f"{self._bullets(self._get(critic, 'challenged_assumptions'))}\n"
                f"**Key Objections Identified by Skeptics:**\n"
                f"{self._bullets(self._get(critic, 'objections'))}"
            )
        )

        # --- SECTION 18: Failure Scenarios ---
        sec_18 = ReportSection(
            title=titles[18],
            content_markdown=(
                f"## {titles[18]}\n\n"
                f"**Stress-Test Failure Scenarios:**\n"
                f"{self._bullets(self._get(critic, 'failure_scenarios'))}\n"
                f"**Early Warning Indicators:**\n"
                f"- Inability to maintain organic repeat usage without continuous promotional subsidies.\n"
                f"- High acquisition churn indicating weak problem urgency or mismatched positioning."
            )
        )

        # --- SECTION 19: Execution Roadmap ---
        sec_19 = ReportSection(
            title=titles[19],
            content_markdown=(
                f"## {titles[19]}\n\n"
                f"**High-Level Phased Execution Steps:**\n"
                f"{self._bullets(self._get(commander, 'execution_plan'))}\n"
                f"**Phase 1 (Months 1-3):** Problem validation & MVP deployment in initial target cluster in {country}.\n"
                f"**Phase 2 (Months 4-6):** Unit economic calibration & retention proof.\n"
                f"**Phase 3 (Months 7-12):** Channel expansion and regional scale-up."
            )
        )

        # --- SECTION 20: Final Recommendation ---
        sec_20 = ReportSection(
            title=titles[20],
            content_markdown=(
                f"## {titles[20]}\n\n"
                f"**Venture Studio Verdict:** {verdict}\n\n"
                f"**Strategic Directives:**\n"
                f"{final_call}\n\n"
                f"**Execution Priorities:**\n"
                f"{self._bullets(self._get(commander, 'execution_plan'))}\n"
                f"**Critical Success Factors:**\n"
                f"{self._bullets(self._get(commander, 'success_factors'))}"
            )
        )

        # --- SECTION 21: Sources & Citations ---
        sec_21 = ReportSection(
            title=titles[21],
            content_markdown=(
                f"## {titles[21]}\n\n"
                f"{self._citation_markdown(citations)}\n\n"
                f"**Research Methodology:**\n"
                f"Evidence collected via autonomous multi-agent reconnaissance, market web intelligence in {country}, "
                f"and curated venture evaluation frameworks. Quantitative figures without verified source citations "
                f"are labeled as estimates, assumptions, or proposed targets."
            ),
            citations=citations
        )

        # Build list of all 21 sections in precise order
        all_sections: List[ReportSection] = [
            sec_1, sec_2, sec_3, sec_4, sec_5,
            sec_6, sec_7, sec_8, sec_9, sec_10,
            sec_11, sec_12, sec_13, sec_14, sec_15,
            sec_16, sec_17, sec_18, sec_19, sec_20,
            sec_21
        ]

        # SWOT section for backward compatibility
        swot_section = ReportSection(
            title="SWOT Analysis",
            content_markdown=(
                "## SWOT Analysis\n\n"
                "**Strengths**\n"
                f"{self._bullets(swot.strengths)}\n"
                "**Weaknesses**\n"
                f"{self._bullets(swot.weaknesses)}\n"
                "**Opportunities**\n"
                f"{self._bullets(swot.opportunities)}\n"
                "**Threats**\n"
                f"{self._bullets(swot.threats)}"
            )
        )

        # Construct full ExecutiveReport preserving all legacy fields AND adding sections array
        report = ExecutiveReport(
            idea_name=idea.company_name,
            version_tag="v1.0",
            battle_score=score,
            confidence_score=conf,
            verdict=verdict,
            executive_summary=sec_1,
            market_research=sec_4,
            swot_analysis=swot_section,
            competitor_analysis=sec_7,
            pricing_strategy=sec_10,
            financial_analysis=sec_11,
            go_to_market_strategy=sec_14,
            critic_analysis=sec_16,
            evidence_citations=sec_21,
            final_recommendation=sec_20,
            market_analysis=sec_4,
            risk_analysis=sec_16,
            recommendations=sec_20,
            target_market=country,
            currency=currency_code,
            currency_symbol=currency_sym,
            sections=all_sections,
            generated_at=datetime.utcnow().isoformat(),
            report_id=run_id,
        )

        json_path = JsonExporter.export(report, self.output_dir)
        md_path = MarkdownExporter.export(report, self.output_dir)
        try:
            pdf_path = PdfExporter.export(md_path, self.output_dir, run_id)
        except Exception as e:
            print(f"PDF Export Failed: {e}")
            pdf_path = None

        manifest_path = self._write_manifest(run_id, idea.company_name, report, pdf_path, json_path, md_path)
        await event_bus.publish(AppEvent(
            event_type=EventType.REPORT_GENERATED,
            run_id=run_id,
            timestamp=datetime.utcnow(),
            data={
                "report_id": run_id,
                "manifest_path": f"/outputs/reports/{os.path.basename(manifest_path)}",
                "pdf_path": f"/outputs/reports/{os.path.basename(pdf_path)}" if pdf_path else None,
                "json_path": f"/outputs/reports/{os.path.basename(json_path)}",
                "md_path": f"/outputs/reports/{os.path.basename(md_path)}",
            },
        ))

        state["swot_analysis"] = swot
        state["gtm_strategy"] = gtm
        state["final_report"] = report.model_dump()
        return state

    def _data(self, output: Any) -> Any:
        return getattr(output, "data", output)

    def _get(self, obj: Any, key: str, default: Any = None) -> Any:
        if obj is None:
            return default
        value = getattr(obj, key, default)
        return default if value is None else value

    def _items(self, value: Any) -> List[Any]:
        if not value:
            return []
        return value if isinstance(value, list) else [value]

    def _text(self, value: Any) -> str:
        if value is None:
            return ""
        if hasattr(value, "model_dump"):
            value = value.model_dump()
        if isinstance(value, dict):
            for key in ("name", "title", "label", "company_name"):
                if value.get(key):
                    text = str(value.get(key)).strip()
                    category = str(value.get("category") or value.get("type") or "").strip()
                    return f"{text} ({category})" if category else text
            return ", ".join(self._text(item) for item in value.values() if item)
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

    def _number(self, value: Any) -> float:
        try:
            return float(value or 0)
        except (TypeError, ValueError):
            return 0.0

    def _bullets(self, values: Any) -> str:
        items = [self._text(v) for v in self._items(values) if self._text(v)]
        return "".join(f"- {item}\n" for item in items) if items else "- Insufficient verified data; requires validation.\n"

    def _sentence(self, values: Any, fallback: str) -> str:
        items = self._items(values)
        first = self._text(items[0]) if items else ""
        return first or fallback

    def _competitor_bullets(self, competitors: Any, startup_name: str = "") -> str:
        rows = []
        seen = set()
        startup_terms = {startup_name.strip().lower()}
        startup_terms.update({term for term in startup_name.lower().replace("/", " ").replace("-", " ").split() if len(term) > 2})
        for comp in self._items(competitors):
            name = self._text(self._get(comp, "name", "Unknown"))
            category = self._text(self._get(comp, "category", "Competitor"))
            if not name:
                continue
            normalized_name = str(name).strip().lower()
            if normalized_name in seen:
                continue
            seen.add(normalized_name)
            if normalized_name in startup_terms or any(term and term in normalized_name for term in startup_terms):
                continue
            strengths = ", ".join(self._text(item) for item in self._items(self._get(comp, "strengths")) if self._text(item)) or "not listed"
            weaknesses = ", ".join(self._text(item) for item in self._items(self._get(comp, "weaknesses")) if self._text(item)) or "not listed"
            geography = self._text(self._get(comp, "geography", ""))
            geo_tag = f" [{geography}]" if geography else ""
            rows.append(f"- **{name}** ({category}){geo_tag} - Strengths: {strengths}. Weaknesses: {weaknesses}.")
        return "\n".join(rows) + "\n" if rows else "- Insufficient verified data; requires validation.\n"

    def _collect_citations(self, scout: Any, analyst: Any) -> List[CitationMapping]:
        mappings = []
        seen = set()
        for source in [scout, analyst]:
            for cit in self._items(self._get(source, "citations")):
                url = self._get(cit, "url")
                title = self._get(cit, "title", url)
                if not url or url in seen:
                    continue
                seen.add(url)
                mappings.append(CitationMapping(id=f"C{len(mappings) + 1}", source_url=url, snippet=title))
        return mappings

    def _citation_markdown(self, citations: List[CitationMapping]) -> str:
        if not citations:
            return "- No external citations attached (analysis based on venture frameworks).\n"
        return "".join(f"- [{c.id}] {c.snippet}: {c.source_url}\n" for c in citations)

    def _final_call(self, verdict: str, score: float, critic: Any) -> str:
        risk = str(self._get(critic, "risk_level", "Medium")).lower()
        if score >= 75 and risk not in {"critical", "high"}:
            return "Proceed with a focused pilot and scale only after retention and unit economics are proven."
        if score >= 60:
            return "Proceed cautiously: validate the riskiest assumptions before committing major capital."
        return "Do not scale yet; redesign the wedge, economics, or positioning before launch."

    def _write_manifest(self, run_id: str, idea: str, report: ExecutiveReport, pdf_path: str | None, json_path: str, md_path: str) -> str:
        manifest = {
            "report_id": run_id,
            "idea": idea,
            "battle_score": report.battle_score,
            "confidence": report.confidence_score,
            "pdf_path": pdf_path,
            "json_path": json_path,
            "md_path": md_path,
            "generated_at": report.generated_at,
        }
        manifest_path = os.path.join(self.output_dir, f"manifest_{run_id}.json")
        with open(manifest_path, "w", encoding="utf-8") as f:
            json.dump(manifest, f, indent=2)
        return manifest_path


report_builder = ReportBuilder()

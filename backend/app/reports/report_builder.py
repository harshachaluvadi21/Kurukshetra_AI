import json
import os
import re
from datetime import datetime
from typing import Any, List

from app.events.event_bus import event_bus
from app.events.event_types import AppEvent, EventType
from app.graph.state import GraphState
from app.reports.exporters.json_exporter import JsonExporter
from app.reports.exporters.markdown_exporter import MarkdownExporter
from app.reports.exporters.pdf_exporter import PdfExporter
from app.reports.models import CitationMapping, ExecutiveReport, ReportSection
from app.services.business_intelligence import build_gtm_strategy, build_swot


class ReportBuilder:
    def __init__(self):
        self.output_dir = os.path.join(os.path.dirname(__file__), "..", "..", "outputs", "reports")
        os.makedirs(self.output_dir, exist_ok=True)

    async def build(self, state: GraphState) -> GraphState:
        run_id = state.get("run_id", "unknown")
        idea = state.get("startup_idea")
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

        executive_summary = ReportSection(
            title="Executive Summary",
            content_markdown=(
                "# Executive Summary\n\n"
                f"**Idea:** {idea.company_name}\n\n"
                f"**Business Concept:** {idea.business_concept}\n\n"
                f"**Verdict:** {verdict}\n\n"
                f"**Battle Score:** {score}/100\n\n"
                f"**Confidence:** {conf * 100:.0f}%\n\n"
                f"**Recommendation:** {final_call}\n\n"
                f"**Top Strengths:** {top_strength}\n\n"
                f"**Top Risks:** {top_risk}\n\n"
                f"**Top Actions:**\n{top_actions}\n"
                f"**Why now:** {self._sentence(self._get(scout, 'trends'), 'Market timing requires validation.')}\n"
            ),
        )

        market_research = ReportSection(
            title="Market Research",
            content_markdown=(
                "## Market Research\n\n"
                f"- **Industry:** {self._get(scout, 'industry', idea.industry)}\n"
                f"- **Estimated TAM:** ${self._number(self._get(scout, 'market_size_usd')):,.0f}\n"
                f"- **Estimated Growth Rate:** {self._number(self._get(scout, 'growth_rate'))}%\n\n"
                "**Key Trends**\n"
                f"{self._bullets(self._get(scout, 'trends'))}\n"
                "**Customer Behavior**\n"
                f"{self._bullets(self._get(scout, 'customer_behavior'))}\n"
                "**Regional Opportunities**\n"
                f"{self._bullets(self._get(scout, 'regional_opportunities'))}"
            ),
            citations=citations,
        )

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
            ),
        )

        competitor_analysis = ReportSection(
            title="Competitor Analysis",
            content_markdown=(
                "## Competitor Analysis\n\n"
                "**Direct Competitors**\n"
                f"{self._competitor_bullets(self._get(analyst, 'direct_competitors'), startup_name)}\n"
                "**Indirect Competitors**\n"
                f"{self._competitor_bullets(self._get(analyst, 'indirect_competitors'), startup_name)}\n"
                "**Feature Gaps**\n"
                f"{self._bullets(self._get(analyst, 'feature_gaps'))}\n"
                "**Market Threats**\n"
                f"{self._bullets(self._get(analyst, 'market_threats'))}"
            ),
            citations=citations,
        )

        pricing_strategy = ReportSection(
            title="Pricing Strategy",
            content_markdown=(
                "## Pricing Strategy\n\n"
                f"- **Recommended Model:** {self._get(treasury, 'pricing_model', 'Not generated')}\n"
                f"- **Revenue Model Submitted:** {idea.revenue_model or 'Not provided'}\n"
                f"- **CAC Guardrail:** ${self._number(self._get(treasury, 'estimated_cac')):,.0f}\n"
                f"- **LTV Target:** ${self._number(self._get(treasury, 'estimated_ltv')):,.0f}\n"
                f"- **Break-even Target:** {self._number(self._get(treasury, 'break_even_months')):.0f} months\n"
            ),
        )

        financial_analysis = ReportSection(
            title="Financial Analysis",
            content_markdown=(
                "## Financial Analysis\n\n"
                f"- **Projected Year 1 Revenue:** ${self._number(self._get(treasury, 'projected_revenue_year_1')):,.0f}\n"
                f"- **Projected Year 3 Revenue:** ${self._number(self._get(treasury, 'projected_revenue_year_3')):,.0f}\n"
                f"- **Estimated CAC:** ${self._number(self._get(treasury, 'estimated_cac')):,.0f}\n"
                f"- **Estimated LTV:** ${self._number(self._get(treasury, 'estimated_ltv')):,.0f}\n"
                f"- **Break-even:** {self._number(self._get(treasury, 'break_even_months')):.0f} months\n"
                f"- **LTV/CAC Ratio:** {self._ltv_cac(treasury)}\n"
            ),
        )

        go_to_market = ReportSection(
            title="Go-To-Market Strategy",
            content_markdown=(
                "## Go-To-Market Strategy\n\n"
                "**Target Customers**\n"
                f"{self._bullets(gtm.target_customers)}\n"
                f"**Positioning**\n\n{gtm.positioning}\n\n"
                "**Channels**\n"
                f"{self._bullets(gtm.channels)}\n"
                "**Customer Acquisition**\n"
                f"{self._bullets(gtm.customer_acquisition)}\n"
                "**Launch Plan**\n"
                f"{self._bullets(gtm.launch_plan)}\n"
                "**Growth Strategy**\n"
                f"{self._bullets(gtm.growth_strategy)}"
            ),
        )

        critic_analysis = ReportSection(
            title="Critic Analysis",
            content_markdown=(
                "## Critic Analysis\n\n"
                f"- **Risk Level:** {self._get(critic, 'risk_level', 'Not generated')}\n\n"
                "**Failure Risks**\n"
                f"{self._bullets(self._get(critic, 'failure_risks'))}\n"
                "**Challenged Assumptions**\n"
                f"{self._bullets(self._get(critic, 'challenged_assumptions'))}\n"
                "**Objections**\n"
                f"{self._bullets(self._get(critic, 'objections'))}\n"
                "**Failure Scenarios**\n"
                f"{self._bullets(self._get(critic, 'failure_scenarios'))}\n"
                "**Mitigation Recommendations**\n"
                f"{self._bullets(self._get(critic, 'mitigation_recommendations'))}"
            ),
        )

        evidence_citations = ReportSection(
            title="Evidence & Citations",
            content_markdown="## Evidence & Citations\n\n" + self._citation_markdown(citations),
            citations=citations,
        )

        final_recommendation = ReportSection(
            title="Final Recommendation",
            content_markdown=(
                "## Final Recommendation\n\n"
                f"{final_call}\n\n"
                "**Execution Priorities**\n"
                f"{self._bullets(self._get(commander, 'execution_plan'))}\n"
                "**Success Factors**\n"
                f"{self._bullets(self._get(commander, 'success_factors'))}"
            ),
        )

        report = ExecutiveReport(
            idea_name=idea.company_name,
            version_tag="v1.0",
            battle_score=score,
            confidence_score=conf,
            verdict=verdict,
            executive_summary=executive_summary,
            market_research=market_research,
            swot_analysis=swot_section,
            competitor_analysis=competitor_analysis,
            pricing_strategy=pricing_strategy,
            financial_analysis=financial_analysis,
            go_to_market_strategy=go_to_market,
            critic_analysis=critic_analysis,
            evidence_citations=evidence_citations,
            final_recommendation=final_recommendation,
            market_analysis=market_research,
            risk_analysis=critic_analysis,
            recommendations=final_recommendation,
            generated_at=datetime.utcnow().isoformat(),
            report_id=run_id,
        )

        json_path = JsonExporter.export(report, self.output_dir)
        md_path = MarkdownExporter.export(report, self.output_dir)
        try:
            pdf_path = PdfExporter.export(md_path, self.output_dir, run_id)
        except Exception as e:
            print(f"PDF Export Failed (missing Weasyprint GTK3?): {e}")
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
        return "".join(f"- {item}\n" for item in items) if items else "- Not generated\n"

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
            rows.append(f"- **{name}** ({category}) - Strengths: {strengths}. Weaknesses: {weaknesses}.")
        return "\n".join(rows) + "\n" if rows else "- Not generated\n"

    def _ltv_cac(self, treasury: Any) -> str:
        cac = self._number(self._get(treasury, "estimated_cac"))
        ltv = self._number(self._get(treasury, "estimated_ltv"))
        return "Not generated" if cac <= 0 else f"{ltv / cac:.2f}x"

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
            return "- No citations attached.\n"
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

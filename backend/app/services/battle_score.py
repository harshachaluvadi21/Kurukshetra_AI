from datetime import datetime
from app.graph.state import GraphState
from app.schemas.score import BattleScore
from app.core.settings import settings
from app.events.event_bus import event_bus
from app.events.event_types import AppEvent, EventType

from app.services.market_context import detect_market_context

class BattleScoreEngine:

    async def calculate(self, state: GraphState) -> dict:
        run_id = state.get("run_id", "unknown")
        idea = state.get("startup_idea")
        market_ctx = detect_market_context(idea)

        # Extract data safely
        scout_resp = state.get("scout_output")
        scout_data = scout_resp.data if scout_resp and getattr(scout_resp, "data", None) else None
        
        analyst_resp = state.get("analyst_output")
        analyst_data = analyst_resp.data if analyst_resp and getattr(analyst_resp, "data", None) else None
        
        treasury_resp = state.get("treasury_output")
        treasury_data = treasury_resp.data if treasury_resp and getattr(treasury_resp, "data", None) else None
        
        # 1. Market Opportunity (Market-aware TAM benchmark & growth rate)
        market_opp = 50.0
        if scout_data:
            # Use local market benchmark (e.g., INR 1,000 Cr in India, $1B in US)
            tam = float(getattr(scout_data, "market_size_local", None) or getattr(scout_data, "market_size_usd", 0.0) or 0.0)
            growth = float(getattr(scout_data, "growth_rate", 0.0) or 0.0)
            benchmark = market_ctx.tam_benchmark_local
            
            tam_ratio = tam / benchmark if benchmark > 0 else 0.5
            tam_score = min(35.0, tam_ratio * 25.0)  # Up to 35 pts
            growth_score = min(15.0, (growth / 20.0) * 15.0)  # Up to 15 pts for 20%+ CAGR
            
            # Prudence discount if data is unverified
            tam_status = str(getattr(scout_data, "tam_status", "")).lower()
            unverified_penalty = 5.0 if "insufficient" in tam_status else 0.0
            
            market_opp = max(25.0, min(100.0, 50.0 + tam_score + growth_score - unverified_penalty))

        # 2. Competition Difficulty (Market-aware competitor saturation)
        comp_diff = 70.0
        if analyst_data:
            direct = getattr(analyst_data, "direct_competitors", [])
            indirect = getattr(analyst_data, "indirect_competitors", [])
            num_direct = len(direct)
            num_indirect = len(indirect)
            
            # Check for dominant incumbents
            incumbents = [c for c in direct if "incumbent" in str(getattr(c, "category", "")).lower()]
            incumbent_penalty = len(incumbents) * 5.0
            
            comp_diff = max(20.0, min(95.0, 90.0 - (num_direct * 7.0) - (num_indirect * 2.5) - incumbent_penalty))

        # 3. Revenue Potential & Unit Economics (Currency-calibrated Y3 Rev + LTV/CAC margin)
        rev_pot = 50.0
        if treasury_data:
            rev_y3 = float(getattr(treasury_data, "projected_revenue_year_3", 0.0) or 0.0)
            rev_benchmark = market_ctx.rev_y3_benchmark_local
            rev_ratio = rev_y3 / rev_benchmark if rev_benchmark > 0 else 0.5
            rev_score = min(35.0, rev_ratio * 25.0)
            
            # Evaluate Unit Economics & Margins
            cac = float(getattr(treasury_data, "estimated_cac", 0.0) or 0.0)
            ltv = float(getattr(treasury_data, "estimated_ltv", 0.0) or 0.0)
            ltv_cac_ratio = (ltv / cac) if cac > 0 else 2.5
            
            if ltv_cac_ratio >= 4.0:
                unit_econ_bonus = 15.0
            elif ltv_cac_ratio >= 3.0:
                unit_econ_bonus = 10.0
            elif ltv_cac_ratio >= 2.0:
                unit_econ_bonus = 5.0
            elif ltv_cac_ratio < 1.2:
                unit_econ_bonus = -15.0
            else:
                unit_econ_bonus = 0.0
                
            rev_pot = max(20.0, min(100.0, 45.0 + rev_score + unit_econ_bonus))
            
        # 4. Investment Readiness (dynamic based on break-even)
        invest_ready = 50.0
        if treasury_data:
            months = float(getattr(treasury_data, "break_even_months", 24) or 24)
            if months <= 12: invest_ready = 90.0
            elif months <= 18: invest_ready = 82.0
            elif months <= 24: invest_ready = 75.0
            elif months <= 36: invest_ready = 60.0
            else: invest_ready = 40.0
        
        # Debate results impact execution and risk
        # For mock, we check if debate_records has items
        debate_records = state.get("debate_records", [])
        
        exec_complex = max(20.0, 80.0 - (len(debate_records) * 3.0)) # Penalize execution complexity if many debates
        critic_output = state.get("critic_output")
        critic_risk = ""
        if critic_output and getattr(critic_output, "data", None):
            critic_risk = getattr(critic_output.data, "risk_level", "")
        risk_penalty = {"low": 5.0, "medium": 15.0, "high": 30.0, "critical": 45.0}.get(str(critic_risk).lower(), 15.0)
        risk_level = min(100.0, 45.0 + risk_penalty + (len(debate_records) * 3.0))

        # Calculate composite score
        composite = (
            (market_opp * settings.WEIGHT_MARKET_OPPORTUNITY) +
            (comp_diff * settings.WEIGHT_COMPETITION_DIFFICULTY) +
            (rev_pot * settings.WEIGHT_REVENUE_POTENTIAL) +
            (exec_complex * settings.WEIGHT_EXECUTION_COMPLEXITY) +
            (invest_ready * settings.WEIGHT_INVESTMENT_READINESS) +
            ((100 - risk_level) * settings.WEIGHT_RISK_LEVEL)
        )

        score_obj = BattleScore(
            market_opportunity=market_opp,
            competition_difficulty=comp_diff,
            revenue_potential=rev_pot,
            execution_complexity=exec_complex,
            investment_readiness=invest_ready,
            risk_level=risk_level,
            composite_score=round(composite, 2)
        )
        
        # Generate Verdict
        verdict = self._generate_verdict(composite)
        pivot_mandated = composite < 40 or str(critic_risk).lower() == "critical"

        # Publish Event
        await event_bus.publish(AppEvent(
            event_type=EventType.SCORE_GENERATED,
            run_id=run_id,
            timestamp=datetime.utcnow(),
            data={
                "score": score_obj.composite_score,
                "verdict": verdict,
                "pivot_mandated": pivot_mandated
            }
        ))
        await event_bus.publish(AppEvent(
            event_type=EventType.VERDICT_GENERATED,
            run_id=run_id,
            timestamp=datetime.utcnow(),
            data={"verdict": verdict}
        ))

        return {
            "battle_score": score_obj,
            "battle_verdict": verdict,
            "pivot_mandated": pivot_mandated,
            "execution_logs": ["Battle Score Engine executed successfully."]
        }

    def _generate_verdict(self, score: float) -> str:
        if score >= 90: return "Exceptional Opportunity"
        if score >= 75: return "Strong Opportunity"
        if score >= 60: return "Promising but Needs Validation"
        if score >= 40: return "High Risk"
        return "Pivot Recommended"

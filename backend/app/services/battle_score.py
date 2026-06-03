from datetime import datetime
from app.graph.state import GraphState
from app.schemas.score import BattleScore
from app.core.settings import settings
from app.events.event_bus import event_bus
from app.events.event_types import AppEvent, EventType

class BattleScoreEngine:

    async def calculate(self, state: GraphState) -> dict:
        run_id = state.get("run_id", "unknown")

        # In V1 we use deterministic heuristic scoring based on mock inputs.
        # In future versions, LLMs will evaluate these dimensions.
        
        # 1. Base scores out of 100
        market_opp = 85.0 if state.get("scout_output") else 50.0
        comp_diff = 70.0 if state.get("analyst_output") else 50.0
        rev_pot = 80.0 if state.get("treasury_output") else 50.0
        
        # Debate results impact execution and risk
        # For mock, we check if debate_records has items
        debate_records = state.get("debate_records", [])
        
        exec_complex = 65.0 - (len(debate_records) * 2.0) # Penalize complexity if many debates
        invest_ready = 75.0
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

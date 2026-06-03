from datetime import datetime
from app.graph.state import GraphState
from app.schemas.score import ConfidenceScore
from app.events.event_bus import event_bus
from app.events.event_types import AppEvent, EventType

class ConfidenceEngine:
    async def evaluate(self, state: GraphState) -> dict:
        run_id = state.get("run_id", "unknown")
        
        # 1. Source Confidence (Check presence of outputs)
        sources_present = sum([
            1 if state.get("scout_output") else 0,
            1 if state.get("analyst_output") else 0,
            1 if state.get("treasury_output") else 0
        ])
        source_conf = sources_present / 3.0 if sources_present > 0 else 0.0
        
        # 2. Debate Confidence (Mock logic: depends on debate participation)
        debate_records = state.get("debate_records", [])
        debate_conf = 0.8 if len(debate_records) >= 2 else 0.4
        
        # 3. Reasoning Confidence
        reasoning_conf = 0.75
        
        # 4. Overall Confidence (Weighted average)
        overall = (source_conf * 0.4) + (debate_conf * 0.3) + (reasoning_conf * 0.3)

        conf_obj = ConfidenceScore(
            source_confidence=round(source_conf, 2),
            debate_confidence=round(debate_conf, 2),
            reasoning_confidence=round(reasoning_conf, 2),
            overall_confidence=round(overall, 2)
        )

        # Publish Event
        await event_bus.publish(AppEvent(
            event_type=EventType.CONFIDENCE_GENERATED,
            run_id=run_id,
            timestamp=datetime.utcnow(),
            data={
                "overall_confidence": conf_obj.overall_confidence
            }
        ))

        return {
            "confidence_score": conf_obj,
            "execution_logs": ["Confidence Engine executed successfully."]
        }

import asyncio
import sys
import os
import uuid

# Adjust Python path to run directly from the scripts folder
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.graph.main_graph import graph
from app.graph.state import GraphState
from app.schemas.project import StartupIdea, ProjectVersion
from app.events.event_bus import event_bus
from app.events.event_types import AppEvent, EventType

async def mock_websocket_subscriber(event: AppEvent):
    if event.event_type in [EventType.SCORE_GENERATED, EventType.CONFIDENCE_GENERATED, EventType.VERDICT_GENERATED]:
        print(f"[EventStream] {event.timestamp.time()} | {event.event_type.value.upper()} | Payload: {event.data}")

async def main():
    print("--- Milestone 4: Battle Score & Confidence Engine Verification ---")
    
    for event_type in [t for t in AppEvent.model_fields['event_type'].annotation]:
        event_bus.subscribe(event_type, mock_websocket_subscriber)
    
    project_id = str(uuid.uuid4())
    run_id = str(uuid.uuid4())
    idea = StartupIdea(company_name="EduAI", business_concept="AI attendance", industry="EdTech")
    version = ProjectVersion(version_tag="v1.0", idea=idea)
    
    initial_state = GraphState(
        run_id=run_id,
        project_id=project_id,
        startup_idea=idea,
        idea_version=version,
        scout_output=None,
        analyst_output=None,
        treasury_output=None,
        debate_records=[],
        battle_score=None,
        battle_verdict=None,
        confidence_score=None,
        final_report=None,
        pivot_mandated=False,
        errors=[],
        execution_logs=[]
    )
    
    print("\n--- Executing Full Main Graph ---")
    final_state = await graph.ainvoke(initial_state)
    
    print("\n--- Final GraphState Outputs ---")
    bs = final_state.get('battle_score')
    cs = final_state.get('confidence_score')
    verdict = final_state.get('battle_verdict')
    pivot = final_state.get('pivot_mandated')
    
    if bs:
        print(f"\n[Battle Score] Composite: {bs.composite_score}/100")
        print(f"  Market: {bs.market_opportunity}, Competition: {bs.competition_difficulty}")
        print(f"  Revenue: {bs.revenue_potential}, Execution: {bs.execution_complexity}")
        print(f"  Investment: {bs.investment_readiness}, Risk: {bs.risk_level}")
        
    if cs:
        print(f"\n[Confidence Score] Overall: {cs.overall_confidence*100}%")
        print(f"  Source: {cs.source_confidence}, Debate: {cs.debate_confidence}, Reasoning: {cs.reasoning_confidence}")
        
    print(f"\n[Verdict] {verdict}")
    print(f"[Pivot Mandated] {pivot}")

if __name__ == "__main__":
    asyncio.run(main())

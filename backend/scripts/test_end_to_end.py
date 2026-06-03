import asyncio
import sys
import os
import uuid
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.graph.main_graph import graph
from app.graph.state import GraphState
from app.schemas.project import StartupIdea, ProjectVersion
from app.events.event_bus import event_bus
from app.events.event_types import AppEvent

async def mock_websocket_subscriber(event: AppEvent):
    # Skip noisy events, focus on milestones
    print(f"[{event.event_type.value.upper()}] {event.data.get('agent_name') or event.data.get('speaker') or ''} {event.data.get('message') or ''}")

async def main():
    print("==========================================================")
    print(" KURUKSHETRA AI - FIRST TRUE BATTLEFIELD RUN ")
    print("==========================================================")
    
    if not os.environ.get("GOOGLE_API_KEY"):
        print("WARNING: GOOGLE_API_KEY is missing! The run will gracefully fail without it.")
        
    for event_type in [t for t in AppEvent.model_fields['event_type'].annotation]:
        event_bus.subscribe(event_type, mock_websocket_subscriber)
    
    project_id = str(uuid.uuid4())
    run_id = str(uuid.uuid4())
    idea = StartupIdea(
        company_name="EduAI", 
        business_concept="AI Attendance System for Colleges.", 
        industry="EdTech"
    )
    version = ProjectVersion(version_tag="v1.0", idea=idea)
    
    initial_state = GraphState(
        run_id=run_id,
        project_id=project_id,
        startup_idea=idea,
        idea_version=version,
        commander_output=None,
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
    
    print(f"\n--- Executing Run: {run_id} ---")
    final_state = await graph.ainvoke(initial_state)
    
    print("\n==========================================================")
    print(" FINAL GRAPH STATE REPORT ")
    print("==========================================================")
    
    if final_state.get('errors'):
        print("\n[ERRORS DETECTED]")
        for err in final_state['errors']:
            print(f"- {err}")
    else:
        print("\n[INTELLIGENCE CAPTURE]")
        if final_state.get('scout_output'):
            print("SCOUT:")
            print(f"  Confidence: {final_state['scout_output'].confidence}")
            print(f"  Industry: {final_state['scout_output'].data.industry}")
            print(f"  Market Size: ${final_state['scout_output'].data.market_size_usd:,.2f}")
            print(f"  Sources: {final_state['scout_output'].sources}")
            
        if final_state.get('analyst_output'):
            print("\nANALYST:")
            print(f"  Confidence: {final_state['analyst_output'].confidence}")
            print(f"  Direct Competitors: {[c.name for c in final_state['analyst_output'].data.direct_competitors]}")
            
        if final_state.get('treasury_output'):
            print("\nTREASURY:")
            print(f"  Confidence: {final_state['treasury_output'].confidence}")
            print(f"  Pricing Model: {final_state['treasury_output'].data.pricing_model}")
            print(f"  Est. CAC: ${final_state['treasury_output'].data.estimated_cac:,.2f}")
            
    if final_state.get('debate_records'):
        print("\n[DEBATE TRANSCRIPT]")
        for rec in final_state['debate_records']:
            print(f"  Round {rec.round_num} | {rec.speaker}: {rec.message}")
            
    if final_state.get('battle_score'):
        print("\n[BATTLE SCORE]")
        print(f"  Composite Score: {final_state['battle_score'].composite_score}/100")
        
    if final_state.get('confidence_score'):
        print("\n[CONFIDENCE SCORE]")
        print(f"  Overall Confidence: {final_state['confidence_score'].overall_confidence*100}%")
        
    print(f"\n[FINAL VERDICT]: {final_state.get('battle_verdict')}")

if __name__ == "__main__":
    asyncio.run(main())

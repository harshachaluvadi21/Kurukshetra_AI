import asyncio
import sys
import os
import uuid
from datetime import datetime

# Adjust Python path to run directly from the scripts folder
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.graph.main_graph import graph
from app.graph.state import GraphState
from app.schemas.project import StartupIdea, ProjectVersion
from app.events.event_bus import event_bus
from app.events.event_types import AppEvent

async def mock_websocket_subscriber(event: AppEvent):
    print(f"[EventStream] {event.timestamp.time()} | {event.event_type.value.upper()} | {event.data.get('agent_name', 'System')}: {event.data.get('message', '')}")

async def main():
    print("--- Milstone 2: LangGraph Foundation Verification ---")
    
    # 1. Subscribe to Event Bus to prove events flow
    for event_type in [t for t in AppEvent.model_fields['event_type'].annotation]:
        event_bus.subscribe(event_type, mock_websocket_subscriber)
    
    # 2. Build initial state
    project_id = str(uuid.uuid4())
    run_id = str(uuid.uuid4())
    idea = StartupIdea(
        company_name="EduAI",
        business_concept="AI attendance system for colleges",
        industry="EdTech"
    )
    version = ProjectVersion(
        version_tag="v1.0",
        idea=idea
    )
    
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
        confidence_score=None,
        final_report=None,
        pivot_mandated=False,
        errors=[],
        execution_logs=[]
    )
    
    print("\n--- Executing Graph ---")
    # 3. Execute Graph
    final_state = await graph.ainvoke(initial_state)
    
    print("\n--- Final GraphState Output ---")
    print(f"Errors: {final_state.get('errors')}")
    print(f"Execution Logs: {final_state.get('execution_logs')}")
    print(f"Scout Output: {final_state.get('scout_output')}")
    print(f"Analyst Output: {final_state.get('analyst_output')}")
    print(f"Treasury Output: {final_state.get('treasury_output')}")

if __name__ == "__main__":
    asyncio.run(main())

import asyncio
import sys
import os
import uuid
import json

# Adjust Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.agents.intelligence_scout import IntelligenceScout
from app.graph.state import GraphState
from app.schemas.project import StartupIdea, ProjectVersion
from app.events.event_bus import event_bus
from app.events.event_types import AppEvent

async def mock_websocket_subscriber(event: AppEvent):
    # Print agent and LLM events
    print(f"[EventStream] {event.timestamp.time()} | {event.event_type.value.upper()} | {event.data.get('agent_name', 'System')}: {event.data.get('message', '')}")

async def main():
    print("--- Milestone 6: Real Intelligence Layer (Intelligence Scout) ---")
    
    # Check for API key
    if not os.environ.get("GOOGLE_API_KEY"):
        print("WARNING: GOOGLE_API_KEY environment variable is not set!")
        print("Please set it in your terminal before running this script.")
        # We will continue, but the Gemini service will likely fail and we'll see the retry/error logic in action.
    
    # Subscribe to Event Bus
    for event_type in [t for t in AppEvent.model_fields['event_type'].annotation]:
        event_bus.subscribe(event_type, mock_websocket_subscriber)
    
    project_id = str(uuid.uuid4())
    run_id = str(uuid.uuid4())
    idea = StartupIdea(
        company_name="EduAI", 
        business_concept="AI-driven automated attendance and engagement tracking for universities.", 
        industry="EdTech"
    )
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
    
    print("\n--- Executing Intelligence Scout Agent (Standalone) ---")
    scout = IntelligenceScout()
    
    # Run the agent directly instead of via the graph for focused testing
    result = await scout.invoke(initial_state)
    
    print("\n--- Final Output ---")
    if result.get("errors"):
        print("Errors encountered:", result["errors"])
    
    output = result.get("scout_output")
    if output:
        print("\nValidated Pydantic LLM Output Envelope:")
        print(f"Confidence: {output.confidence}")
        print(f"Sources: {output.sources}")
        
        print("\nStructured Data (ScoutData):")
        print(f"Industry: {output.data.industry}")
        print(f"Market Size (USD): ${output.data.market_size_usd:,.2f}")
        print(f"Growth Rate (CAGR): {output.data.growth_rate}%")
        print(f"Trends: {output.data.trends}")
    else:
        print("\nNo output returned from agent.")

if __name__ == "__main__":
    asyncio.run(main())

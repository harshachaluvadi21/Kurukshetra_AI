import asyncio
import sys
import os
import uuid
from datetime import datetime

# Adjust Python path to run directly from the scripts folder
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.graph.debate_engine import debate_graph
from app.graph.debate_state import DebateState
from app.events.event_bus import event_bus
from app.events.event_types import AppEvent

async def mock_websocket_subscriber(event: AppEvent):
    # Only print debate events for this test
    if "debate" in event.event_type.value:
        print(f"[EventStream] {event.timestamp.time()} | {event.event_type.value.upper()} | {event.data.get('speaker', 'System')}: {event.data.get('message', '')}")

async def main():
    print("--- Milestone 3: Debate Engine Verification ---")
    
    # 1. Subscribe to Event Bus to prove debate events flow
    for event_type in [t for t in AppEvent.model_fields['event_type'].annotation]:
        event_bus.subscribe(event_type, mock_websocket_subscriber)
    
    # 2. Build initial Debate State
    run_id = str(uuid.uuid4())
    debate_id = str(uuid.uuid4())
    
    initial_state = DebateState(
        run_id=run_id,
        debate_id=debate_id,
        current_round=1,
        max_rounds=2,
        analyst_output=None, # In a real graph, passed from GraphState
        treasury_output=None,
        vulnerabilities=[],
        defenses=[],
        verdict=None,
        pivot_required=False,
        debate_history=[]
    )
    
    print("\n--- Executing Debate Graph (Max 2 Rounds) ---")
    # 3. Execute Graph
    final_state = await debate_graph.ainvoke(initial_state)
    
    print("\n--- Final DebateState Output ---")
    print(f"Total Rounds Executed: {final_state.get('current_round') - 1}")
    print(f"Pivot Required Flag: {final_state.get('pivot_required')}")
    
    print("\n--- Extracted Vulnerabilities ---")
    for v in final_state.get('vulnerabilities', []):
        print(f"- [{v.severity}] {v.issue}")
        
    print("\n--- Extracted Defenses ---")
    for d in final_state.get('defenses', []):
        print(f"- [{d.confidence_level}] {d.counter_argument}")
        
    print("\n--- Verdict ---")
    verdict = final_state.get('verdict')
    if verdict:
        print(f"Winner: {verdict.winner} (Confidence: {verdict.confidence})")
        print(f"Summary: {verdict.summary}")

    print("\n--- Full Debate History ---")
    for h in final_state.get('debate_history', []):
        print(f"Round {h.round_num} | {h.speaker}: {h.message}")

if __name__ == "__main__":
    asyncio.run(main())

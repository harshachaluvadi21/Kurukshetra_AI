import asyncio
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.graph.builder import build_graph
from app.graph.state import GraphState
from app.models.project import StartupIdea
from app.events.event_bus import event_bus

async def main():
    print("==========================================================")
    print(" FIRST FULLY LIVE BATTLE TEST ")
    print("==========================================================")
    
    # 1. Setup subscriber to print events
    def print_event(event):
        # Filter for key events so it's not too spammy
        print(f"[{event.event_type.value}] {event.data.get('agent_name', 'System')} - {event.data.get('message', '')}")
    
    event_bus.subscribe(print_event)
    
    # 2. Build the graph
    app = build_graph()
    
    # 3. Setup Initial State
    initial_state = GraphState({
        "run_id": "live-battle-001",
        "project_id": "proj-live",
        "startup_idea": StartupIdea(
            company_name="EduTrack AI",
            business_concept="AI Attendance System for Colleges",
            industry="EdTech"
        ),
        "idea_version": 1,
        "scout_output": None,
        "analyst_output": None,
        "treasury_output": None,
        "commander_output": None,
        "debate_records": [],
        "battle_score": None,
        "confidence_score": None,
        "final_report": None,
        "pivot_mandated": False,
        "errors": [],
        "execution_logs": []
    })
    
    # 4. Execute
    print("Executing Graph...")
    final_state = await app.ainvoke(initial_state)
    
    print("\n==========================================================")
    print(" FINAL GRAPH STATE REPORT ")
    print("==========================================================")
    
    if final_state["errors"]:
        print("\n[ERRORS DETECTED]")
        for err in final_state["errors"]:
            print(f"- {err}")
            
    print("\n[DEBATE TRANSCRIPT]")
    for record in final_state.get("debate_records", []):
        print(f"  Round {record.round_number} | {record.speaker}: {record.content}")
        
    if final_state.get("battle_score"):
        print("\n[BATTLE SCORE]")
        print(f"  Composite Score: {final_state['battle_score'].composite_score}/100")
        
    if final_state.get("confidence_score"):
        print("\n[CONFIDENCE SCORE]")
        print(f"  Overall Confidence: {final_state['confidence_score'].overall_confidence}%")
        
    if final_state.get("final_report"):
        print(f"\n[FINAL VERDICT]: {final_state['final_report'].verdict}")
        
    print("\n[RAG / EXTERNAL SEARCH INTELLIGENCE METRICS]")
    # Because final_state['scout_output'] might have citations
    scout_data = final_state.get("scout_output")
    if scout_data and scout_data.data.evidence:
        print(f"  Scout Search Citations: {len(scout_data.data.evidence.search_evidence[0].supporting_quotes)}")
        print(f"  Scout Knowledge Base Citations: {len(scout_data.data.evidence.knowledge_evidence[0].supporting_chunks)}")

if __name__ == "__main__":
    asyncio.run(main())

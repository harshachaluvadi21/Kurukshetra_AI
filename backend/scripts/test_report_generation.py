import asyncio
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.graph.state import GraphState
from app.schemas.project import StartupIdea, ProjectVersion
from app.schemas.score import BattleScore, ConfidenceScore
from app.reports.report_builder import report_builder
import uuid
import json

async def test_report():
    run_id = str(uuid.uuid4())
    idea = StartupIdea(company_name="TestIdea", business_concept="A concept.", industry="SaaS")
    
    mock_state = GraphState(
        run_id=run_id,
        project_id="test_proj",
        startup_idea=idea,
        idea_version=ProjectVersion(version_tag="v1.0", idea=idea),
        battle_score=BattleScore(
            market_opportunity=8,
            competition_difficulty=7,
            revenue_potential=9,
            execution_complexity=6,
            investment_readiness=8,
            risk_level=5,
            composite_score=75.0,
            rubric_evaluation="Good"
        ),
        confidence_score=ConfidenceScore(
            source_confidence=0.8,
            debate_confidence=0.9,
            reasoning_confidence=0.85,
            overall_confidence=0.85
        ),
        battle_verdict="Promising",
        errors=[],
        execution_logs=[]
    )
    
    print(f"Building report for Run ID: {run_id}")
    final_state = await report_builder.build(mock_state)
    
    print("Report build completed.")
    
    output_dir = os.path.join(os.path.dirname(__file__), '..', 'outputs', 'reports')
    
    files_to_check = [
        f"report_{run_id}.json",
        f"report_{run_id}.md",
        f"manifest_{run_id}.json"
    ]
    
    # WeasyPrint might fail on Windows without GTK3, so check if PDF is there or not.
    pdf_path = os.path.join(output_dir, f"report_{run_id}.pdf")
    if os.path.exists(pdf_path):
        print(f"PASS: {pdf_path} exists.")
    else:
        print(f"WARNING: {pdf_path} does not exist (likely WeasyPrint exception).")
        
    for f in files_to_check:
        path = os.path.join(output_dir, f)
        if os.path.exists(path):
            print(f"PASS: {path} exists.")
        else:
            print(f"FAIL: {path} does not exist.")
            
if __name__ == "__main__":
    asyncio.run(test_report())

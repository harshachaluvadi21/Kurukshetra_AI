import asyncio
import sys
import os
import json
import time
import uuid

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.graph.main_graph import graph
from app.graph.state import GraphState
from app.schemas.project import StartupIdea, ProjectVersion
from evaluation.metrics import evaluate_run, EvaluationMetrics

# Suppress events to keep logs clean
import logging
logging.getLogger("httpx").setLevel(logging.WARNING)

async def run_evaluation():
    print("==========================================================")
    print(" KURUKSHETRA AI - MILESTONE 10 EVALUATION RUNNER ")
    print("==========================================================")
    
    dataset_path = os.path.join(os.path.dirname(__file__), 'benchmark_dataset.json')
    with open(dataset_path, 'r') as f:
        dataset = json.load(f)
        
    results = []
    
    print(f"Loaded {len(dataset)} startup ideas for evaluation.\n")
    
    for i, item in enumerate(dataset):
        idea_name = item["company_name"]
        print(f"[{i+1}/{len(dataset)}] Evaluating: {idea_name} - {item['business_concept']}")
        
        project_id = str(uuid.uuid4())
        run_id = f"eval-{i+1}"
        
        idea = StartupIdea(
            company_name=idea_name,
            business_concept=item["business_concept"],
            industry=item["industry"]
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
        
        start_time = time.time()
        try:
            # We don't subscribe to the event bus here to keep output clean,
            # but LangSmith will capture the traces automatically.
            final_state = await graph.ainvoke(initial_state)
            latency = time.time() - start_time
            
            metrics = evaluate_run(final_state, latency)
            results.append(metrics.model_dump())
            
            print(f"  -> Score: {metrics.battle_score:.1f} | Conf: {metrics.confidence:.1f}% | Verdict: {metrics.verdict}")
            if metrics.errors:
                print(f"  -> Errors: {len(metrics.errors)} detected")
                
        except Exception as e:
            latency = time.time() - start_time
            print(f"  -> CRITICAL FAILURE: {e}")
            results.append({
                "idea_name": idea_name,
                "battle_score": 0.0,
                "confidence": 0.0,
                "verdict": "FAILED",
                "latency_seconds": latency,
                "search_citation_count": 0,
                "rag_retrieval_count": 0,
                "agent_quality_score": 0,
                "debate_quality_score": 0,
                "citation_quality_score": 0,
                "retrieval_quality_score": 0,
                "errors": [str(e)]
            })
            
        # Optional: Sleep to prevent rate limiting
        await asyncio.sleep(2)
        
    # Save results
    results_path = os.path.join(os.path.dirname(__file__), 'benchmark_results.json')
    with open(results_path, 'w') as f:
        json.dump(results, f, indent=2)
        
    print(f"\nEvaluation Complete! Results saved to {results_path}")

if __name__ == "__main__":
    asyncio.run(run_evaluation())

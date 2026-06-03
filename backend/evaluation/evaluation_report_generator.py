import json
import os
import sys

def generate_report():
    results_path = os.path.join(os.path.dirname(__file__), 'benchmark_results.json')
    if not os.path.exists(results_path):
        print("Run evaluation_runner.py first.")
        return
        
    with open(results_path, 'r') as f:
        results = json.load(f)
        
    total_runs = len(results)
    successful_runs = len([r for r in results if not r['errors']])
    failed_runs = total_runs - successful_runs
    
    avg_latency = sum(r['latency_seconds'] for r in results) / total_runs if total_runs else 0
    avg_battle_score = sum(r['battle_score'] for r in results) / total_runs if total_runs else 0
    avg_confidence = sum(r['confidence'] for r in results) / total_runs if total_runs else 0
    
    avg_agent = sum(r['agent_quality_score'] for r in results) / total_runs if total_runs else 0
    avg_debate = sum(r['debate_quality_score'] for r in results) / total_runs if total_runs else 0
    avg_citation = sum(r['citation_quality_score'] for r in results) / total_runs if total_runs else 0
    avg_retrieval = sum(r['retrieval_quality_score'] for r in results) / total_runs if total_runs else 0
    
    report = f"""# Kurukshetra AI Evaluation Report (Milestone 10)

## 1. System Reliability
- **Total Evaluations:** {total_runs}
- **Successful Runs:** {successful_runs}
- **Failed Runs:** {failed_runs}
- **Error Rate:** {(failed_runs/total_runs)*100 if total_runs else 0:.1f}%
- **Average Latency:** {avg_latency:.2f}s per idea

## 2. Intelligence Quality Metrics (0-5 Scale)
- **Agent Reasoning Quality:** {avg_agent:.1f} / 5.0
- **Debate Depth Quality:** {avg_debate:.1f} / 5.0
- **Search Citation Quality:** {avg_citation:.1f} / 5.0
- **RAG Retrieval Quality:** {avg_retrieval:.1f} / 5.0

## 3. Platform Scoring Calibration
- **Average Battle Score:** {avg_battle_score:.1f}/100
- **Average Confidence:** {avg_confidence:.1f}%

## 4. Failure Analysis
"""
    
    errors = [r for r in results if r['errors']]
    if not errors:
        report += "- No systematic failures detected during execution.\n"
    else:
        for err in errors:
            report += f"- **{err['idea_name']}**: {err['errors'][0]}\n"
            
    report += "\n## 5. Next Steps\n- Proceed to Milestone 11: PDF Report Generation.\n"
    
    report_path = os.path.join(os.path.dirname(__file__), 'evaluation_report.md')
    with open(report_path, 'w') as f:
        f.write(report)
        
    print(f"Report generated at {report_path}")

if __name__ == "__main__":
    generate_report()

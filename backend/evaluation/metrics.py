from typing import Dict, Any, List
from app.graph.state import GraphState
from pydantic import BaseModel

class EvaluationMetrics(BaseModel):
    idea_name: str
    battle_score: float
    confidence: float
    verdict: str
    latency_seconds: float
    search_citation_count: int
    rag_retrieval_count: int
    agent_quality_score: int
    debate_quality_score: int
    citation_quality_score: int
    retrieval_quality_score: int
    errors: List[str]

def evaluate_run(state: GraphState, latency: float) -> EvaluationMetrics:
    """
    Evaluates a single execution using deterministic rubrics based on the final GraphState.
    Note: In a true LLM-as-a-judge setup, we would prompt Gemini to grade this.
    For this framework, we apply heuristic proxies to approximate the 0-5 rubrics.
    """
    idea_name = state.get("startup_idea").company_name if state.get("startup_idea") else "Unknown"
    
    # Extract Search and RAG counts
    scout_out = state.get("scout_output")
    search_citations = 0
    rag_retrievals = 0
    
    if scout_out and hasattr(scout_out, "data") and scout_out.data.evidence:
        search_citations = len(scout_out.data.evidence.search_evidence[0].supporting_citations) if scout_out.data.evidence.search_evidence else 0
        rag_retrievals = len(scout_out.data.evidence.knowledge_evidence[0].supporting_chunks) if scout_out.data.evidence.knowledge_evidence else 0
        
    # Heuristic Agent Quality Score (0-5)
    # 5 if all 3 agents returned confident outputs (>0.8) without errors
    agent_quality = 0
    confidences = []
    for out in [state.get("scout_output"), state.get("analyst_output"), state.get("treasury_output")]:
        if out and hasattr(out, "confidence"):
            confidences.append(out.confidence)
            
    if len(confidences) == 3:
        avg_conf = sum(confidences) / 3.0
        if avg_conf > 0.85: agent_quality = 5
        elif avg_conf > 0.7: agent_quality = 4
        elif avg_conf > 0.5: agent_quality = 3
        else: agent_quality = 2
    elif len(confidences) > 0:
        agent_quality = 1
        
    # Heuristic Debate Quality Score (0-5)
    # Based on number of rounds and depth
    debate_records = state.get("debate_records", [])
    if len(debate_records) >= 6: # 3 full rounds
        debate_quality = 5
    elif len(debate_records) >= 4:
        debate_quality = 4
    elif len(debate_records) >= 2:
        debate_quality = 3
    elif len(debate_records) > 0:
        debate_quality = 2
    else:
        debate_quality = 0
        
    # Heuristic Citation Quality Score (0-5)
    if search_citations >= 5: citation_quality = 5
    elif search_citations >= 3: citation_quality = 4
    elif search_citations >= 1: citation_quality = 3
    else: citation_quality = 0
    
    # Heuristic Retrieval Quality Score (0-5)
    if rag_retrievals >= 3: retrieval_quality = 5
    elif rag_retrievals >= 2: retrieval_quality = 4
    elif rag_retrievals >= 1: retrieval_quality = 3
    else: retrieval_quality = 0
    
    return EvaluationMetrics(
        idea_name=idea_name,
        battle_score=state.get("battle_score").composite_score if state.get("battle_score") else 0.0,
        confidence=state.get("confidence_score").overall_confidence if state.get("confidence_score") else 0.0,
        verdict=state.get("battle_verdict") or "Error",
        latency_seconds=latency,
        search_citation_count=search_citations,
        rag_retrieval_count=rag_retrievals,
        agent_quality_score=agent_quality,
        debate_quality_score=debate_quality,
        citation_quality_score=citation_quality,
        retrieval_quality_score=retrieval_quality,
        errors=state.get("errors", [])
    )

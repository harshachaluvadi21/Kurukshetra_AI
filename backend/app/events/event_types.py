from enum import Enum
from pydantic import BaseModel
from typing import Dict, Any
from datetime import datetime

class EventType(str, Enum):
    RUN_STARTED = "run_started"
    RUN_CREATED = "run_created"
    PROJECT_CREATED = "project_created"
    AGENT_STARTED = "agent_started"
    AGENT_THINKING = "agent_thinking"
    AGENT_COMPLETED = "agent_completed"
    
    DEBATE_STARTED = "debate_started"
    DEBATE_TURN = "debate_turn"
    DEBATE_COMPLETED = "debate_completed"
    
    SCORE_GENERATED = "score_generated"
    CONFIDENCE_GENERATED = "confidence_generated"
    VERDICT_GENERATED = "verdict_generated"
    
    # LLM Events
    LLM_REQUEST_STARTED = "llm_request_started"
    LLM_RESPONSE_RECEIVED = "llm_response_received"
    LLM_VALIDATION_FAILED = "llm_validation_failed"
    LLM_RETRY = "llm_retry"
    LLM_PROVIDER_SELECTED = "llm_provider_selected"
    LLM_FALLBACK_TRIGGERED = "llm_fallback_triggered"
    LLM_PROVIDER_FAILED = "llm_provider_failed"
    LLM_PROVIDER_RECOVERED = "llm_provider_recovered"
    
    # Web Intelligence Events
    SEARCH_STARTED = "search_started"
    SEARCH_COMPLETED = "search_completed"
    SOURCES_RANKED = "sources_ranked"
    CITATIONS_GENERATED = "citations_generated"
    EVIDENCE_GENERATED = "evidence_generated"
    
    # Provider Events
    PROVIDER_REQUEST_STARTED = "provider_request_started"
    PROVIDER_RESPONSE_RECEIVED = "provider_response_received"
    SEARCH_RESULTS_FILTERED = "search_results_filtered"
    SEARCH_RESULTS_RANKED = "search_results_ranked"
    
    # RAG Events
    RAG_RETRIEVAL_STARTED = "rag_retrieval_started"
    RAG_RETRIEVAL_COMPLETED = "rag_retrieval_completed"
    CHUNKS_RETRIEVED = "chunks_retrieved"
    KNOWLEDGE_EVIDENCE_GENERATED = "knowledge_evidence_generated"
    
    RUN_COMPLETED = "run_completed"
    RUN_PIVOTED = "run_pivoted"
    
    # Execution & Reporting Events
    EXECUTION_COMPLETED = "execution_completed"
    EXECUTION_FAILED = "execution_failed"
    REPORT_GENERATED = "report_generated"
    REPORT_FAILED = "report_failed"

class AppEvent(BaseModel):
    event_type: EventType
    run_id: str
    timestamp: datetime
    data: Dict[str, Any]

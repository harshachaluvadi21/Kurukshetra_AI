from pydantic import BaseModel
from typing import List
from app.intelligence.models import SourceEvidence

class KnowledgeChunk(BaseModel):
    chunk_id: str
    source: str
    document_name: str
    category: str
    content: str
    relevance_score: float

class KnowledgeEvidence(BaseModel):
    claim: str
    supporting_chunks: List[KnowledgeChunk]
    confidence: float

class CombinedEvidence(BaseModel):
    search_evidence: List[SourceEvidence]
    knowledge_evidence: List[KnowledgeEvidence]
    combined_confidence: float
    summary: str

from pydantic import BaseModel, Field
from typing import List

class SearchResult(BaseModel):
    title: str
    snippet: str
    url: str
    source_type: str

class Citation(BaseModel):
    title: str = Field(..., description="Title of the source.")
    url: str = Field(..., description="URL of the source.")
    source_type: str = Field(..., description="Classification of the source (e.g. Government, Blog).")
    confidence: float = Field(..., description="Calculated confidence score (0.0 to 1.0).")
    retrieval_timestamp: str = Field(..., description="ISO timestamp of when this was retrieved.")
    provider: str = Field(..., description="Source of intelligence (tavily, serper, knowledge_base)")

class SourceEvidence(BaseModel):
    claim: str
    supporting_citations: List[Citation]
    confidence: float

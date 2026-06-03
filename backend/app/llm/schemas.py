from pydantic import BaseModel, Field
from typing import TypeVar, Generic, List
from typing import TypeVar, Generic, List, Optional, Dict, Any

DataT = TypeVar('DataT')

class AgentLLMResponse(BaseModel, Generic[DataT]):
    """Standardized Agent Output Contract wrapped around specific data."""
    data: DataT = Field(..., description="The specific structured data output by the agent.")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Agent's confidence in this output (0.0 to 1.0).")
    sources: List[str] = Field(default_factory=list, description="List of sources backing this output.")
    provider_metadata: Optional[Dict[str, Any]] = Field(default=None, description="Additional metadata provided by the model provider.")

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class RunCreate(BaseModel):
    project_id: Optional[str] = Field(None, max_length=100)
    idea: str = Field(..., min_length=3, max_length=2000, description="Startup business concept")
    problem_statement: Optional[str] = Field(None, max_length=1000)
    target_users: Optional[str] = Field(None, max_length=1000)
    revenue_model: Optional[str] = Field(None, max_length=1000)

class RunResponse(BaseModel):
    run_id: str
    project_id: Optional[str] = None
    idea: Optional[str] = None
    status: str
    created_at: Optional[datetime] = None

class RunStatusResponse(BaseModel):
    run_id: str
    status: str
    progress: int = 0
    final_state: Optional[dict] = None

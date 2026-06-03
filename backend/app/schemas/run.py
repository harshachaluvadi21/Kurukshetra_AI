from pydantic import BaseModel, UUID4
from typing import Optional
from datetime import datetime

class RunCreate(BaseModel):
    project_id: str
    idea: str
    problem_statement: Optional[str] = None
    target_users: Optional[str] = None
    revenue_model: Optional[str] = None

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

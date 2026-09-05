from pydantic import BaseModel, Field
from typing import Optional

class StartupIdea(BaseModel):
    company_name: str
    business_concept: str
    industry: str
    problem_statement: Optional[str] = None
    target_users: Optional[str] = None
    revenue_model: Optional[str] = None
    target_market: Optional[str] = None
    geography: Optional[str] = None

class ProjectVersion(BaseModel):
    version_tag: str = Field(..., description="e.g., v1.0")
    parent_version_id: Optional[str] = None
    iteration_reason: str = Field(default="Initial Concept")
    idea: StartupIdea

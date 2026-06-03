from pydantic import BaseModel
from typing import List

class Vulnerability(BaseModel):
    issue: str
    severity: str

class Defense(BaseModel):
    counter_argument: str
    confidence_level: str

class DebateVerdict(BaseModel):
    winner: str
    confidence: float
    pivot_required: bool
    summary: str

class DebateHistoryItem(BaseModel):
    round_num: int
    speaker: str
    message: str

from pydantic import BaseModel, Field

class ConfidenceScore(BaseModel):
    source_confidence: float = Field(ge=0, le=1)
    debate_confidence: float = Field(ge=0, le=1)
    reasoning_confidence: float = Field(ge=0, le=1)
    overall_confidence: float = Field(ge=0, le=1)

class BattleScore(BaseModel):
    market_opportunity: float = Field(ge=0, le=100)
    competition_difficulty: float = Field(ge=0, le=100)
    revenue_potential: float = Field(ge=0, le=100)
    execution_complexity: float = Field(ge=0, le=100)
    investment_readiness: float = Field(ge=0, le=100)
    risk_level: float = Field(ge=0, le=100)
    composite_score: float = Field(ge=0, le=100)

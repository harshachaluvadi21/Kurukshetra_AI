from pydantic import BaseModel, Field
from typing import List, Optional
from app.intelligence.models import Citation, SourceEvidence
from app.rag.models import CombinedEvidence

# Scout
class ScoutData(BaseModel):
    industry: str = Field(..., description="The identified broad industry classification.")
    market_size_usd: float = Field(..., description="Estimated TAM in USD.")
    growth_rate: float = Field(..., description="Estimated CAGR percentage.")
    trends: List[str] = Field(..., description="Top 3 macro trends affecting this concept.")
    customer_behavior: List[str] = Field(default_factory=list, description="Observed customer behavior patterns relevant to the concept.")
    regional_opportunities: List[str] = Field(default_factory=list, description="Regions or geographies with the strongest opportunity.")
    citations: List[Citation] = Field(default_factory=list, description="Citations used for this analysis.")
    evidence: Optional[CombinedEvidence] = Field(None, description="Combined evidence package backing this analysis.")

# Analyst
class Competitor(BaseModel):
    name: str = Field(..., description="Competitor company name.")
    category: str = Field(..., description="E.g., Incumbent, Startup, Direct, Indirect.")
    strengths: List[str] = Field(..., description="Core strengths of this competitor.")
    weaknesses: List[str] = Field(..., description="Core weaknesses or vulnerabilities.")

class OpponentAnalystData(BaseModel):
    direct_competitors: List[Competitor] = Field(..., description="List of direct competitors.")
    indirect_competitors: List[Competitor] = Field(..., description="List of indirect or substitute competitors.")
    feature_gaps: List[str] = Field(..., description="Key feature or service gaps in the current market.")
    market_threats: List[str] = Field(..., description="External market threats to the startup.")
    citations: List[Citation] = Field(default_factory=list, description="Citations used for this analysis.")
    evidence: Optional[CombinedEvidence] = Field(None, description="Combined evidence package backing this analysis.")

# Treasury
class TreasuryAdvisorData(BaseModel):
    pricing_model: str = Field(..., description="Proposed pricing strategy (e.g., B2B SaaS per seat).")
    projected_revenue_year_1: float = Field(..., description="Estimated Year 1 revenue in USD.")
    projected_revenue_year_3: float = Field(..., description="Estimated Year 3 revenue in USD.")
    estimated_cac: float = Field(..., description="Estimated Customer Acquisition Cost in USD.")
    estimated_ltv: float = Field(..., description="Estimated Customer Lifetime Value in USD.")
    break_even_months: int = Field(..., description="Estimated months to reach break-even.")
    citations: List[Citation] = Field(default_factory=list, description="Citations used for this analysis.")
    evidence: Optional[CombinedEvidence] = Field(None, description="Combined evidence package backing this analysis.")

# Commander
class StrategyCommanderData(BaseModel):
    industry: str = Field(..., description="Target industry.")
    startup_type: str = Field(..., description="Classification of startup (e.g., DeepTech, Marketplace).")
    execution_plan: List[str] = Field(..., description="High-level phased execution steps.")
    research_priorities: List[str] = Field(..., description="What the other agents should focus on.")
    success_factors: List[str] = Field(..., description="Critical factors for this startup to win.")

class SWOTAnalysis(BaseModel):
    strengths: List[str] = Field(default_factory=list)
    weaknesses: List[str] = Field(default_factory=list)
    opportunities: List[str] = Field(default_factory=list)
    threats: List[str] = Field(default_factory=list)

class GTMStrategy(BaseModel):
    target_customers: List[str] = Field(default_factory=list)
    positioning: str = ""
    channels: List[str] = Field(default_factory=list)
    customer_acquisition: List[str] = Field(default_factory=list)
    launch_plan: List[str] = Field(default_factory=list)
    growth_strategy: List[str] = Field(default_factory=list)

class CriticAnalysisData(BaseModel):
    risk_level: str = Field(..., description="Low, Medium, High, or Critical.")
    failure_risks: List[str] = Field(default_factory=list)
    challenged_assumptions: List[str] = Field(default_factory=list)
    objections: List[str] = Field(default_factory=list)
    failure_scenarios: List[str] = Field(default_factory=list)
    mitigation_recommendations: List[str] = Field(default_factory=list)

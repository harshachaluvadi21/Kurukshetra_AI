from pydantic import BaseModel, Field
from typing import List, Optional
from app.intelligence.models import Citation, SourceEvidence
from app.rag.models import CombinedEvidence

# Scout
class ScoutData(BaseModel):
    industry: str = Field(..., description="The identified broad industry classification.")
    market_size_usd: float = Field(..., description="Estimated TAM in USD or local currency amount.")
    growth_rate: float = Field(..., description="Estimated CAGR percentage.")
    trends: List[str] = Field(..., description="Top 3 macro trends affecting this concept.")
    customer_behavior: List[str] = Field(default_factory=list, description="Observed customer behavior patterns relevant to the concept.")
    regional_opportunities: List[str] = Field(default_factory=list, description="Regions or geographies with the strongest opportunity.")
    currency: Optional[str] = Field(default="INR", description="Currency code (INR, USD, EUR, GBP).")
    market_size_local: Optional[float] = Field(None, description="Estimated TAM in local currency units.")
    tam_status: Optional[str] = Field(default="Estimated", description="Status: User-provided, Source-based, Estimated, Model assumption, Proposed target, or Insufficient verified data; requires validation.")
    sam_som_notes: Optional[str] = Field(default=None, description="SAM / SOM breakdowns or status if verified.")
    citations: List[Citation] = Field(default_factory=list, description="Citations used for this analysis.")
    evidence: Optional[CombinedEvidence] = Field(None, description="Combined evidence package backing this analysis.")

# Analyst
class Competitor(BaseModel):
    name: str = Field(..., description="Competitor company name.")
    category: str = Field(..., description="E.g., Incumbent, Startup, Direct, Indirect.")
    strengths: List[str] = Field(..., description="Core strengths of this competitor.")
    weaknesses: List[str] = Field(..., description="Core weaknesses or vulnerabilities.")
    geography: Optional[str] = Field(default="India", description="Operating market: India, Regional, or Global.")

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
    projected_revenue_year_1: float = Field(..., description="Estimated Year 1 revenue in local currency.")
    projected_revenue_year_3: float = Field(..., description="Estimated Year 3 revenue in local currency.")
    estimated_cac: float = Field(..., description="Estimated Customer Acquisition Cost in local currency.")
    estimated_ltv: float = Field(..., description="Estimated Customer Lifetime Value in local currency.")
    break_even_months: int = Field(..., description="Estimated months to reach break-even.")
    currency: Optional[str] = Field(default="INR", description="Currency code (e.g. INR, USD, GBP, EUR).")
    currency_symbol: Optional[str] = Field(default="₹", description="Currency symbol.")
    financial_status: Optional[str] = Field(default="Model assumption", description="Status of financial figures (Estimated / Model assumption / Proposed target).")
    citations: List[Citation] = Field(default_factory=list, description="Citations used for this analysis.")
    evidence: Optional[CombinedEvidence] = Field(None, description="Combined evidence package backing this analysis.")

# Commander
class StrategyCommanderData(BaseModel):
    industry: str = Field(..., description="Target industry.")
    startup_type: str = Field(..., description="Classification of startup (e.g., DeepTech, Marketplace).")
    execution_plan: List[str] = Field(..., description="High-level phased execution steps.")
    research_priorities: List[str] = Field(..., description="What the other agents should focus on.")
    success_factors: List[str] = Field(..., description="Critical factors for this startup to win.")
    mvp_scope: Optional[List[str]] = Field(default_factory=list, description="Specific MVP deliverables.")
    validation_strategy: Optional[List[str]] = Field(default_factory=list, description="Validation steps to test core assumptions.")
    success_metrics: Optional[List[str]] = Field(default_factory=list, description="North star and pilot KPI targets.")

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

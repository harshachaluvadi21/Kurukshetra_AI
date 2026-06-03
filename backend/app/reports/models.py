from pydantic import BaseModel, Field
from typing import List, Optional

class CitationMapping(BaseModel):
    id: str
    source_url: str
    snippet: str

class ReportSection(BaseModel):
    title: str
    content_markdown: str
    citations: List[CitationMapping] = []

class ExecutiveReport(BaseModel):
    idea_name: str
    version_tag: str
    battle_score: float
    confidence_score: float
    verdict: str
    
    executive_summary: ReportSection
    market_research: ReportSection
    swot_analysis: ReportSection
    competitor_analysis: ReportSection
    pricing_strategy: ReportSection
    financial_analysis: ReportSection
    go_to_market_strategy: ReportSection
    critic_analysis: ReportSection
    evidence_citations: ReportSection
    final_recommendation: ReportSection
    market_analysis: Optional[ReportSection] = None
    risk_analysis: Optional[ReportSection] = None
    recommendations: Optional[ReportSection] = None
    
    generated_at: str
    report_id: str

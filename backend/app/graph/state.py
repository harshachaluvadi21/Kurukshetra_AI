import operator
from typing import TypedDict, Annotated, List, Optional, Any
from app.schemas.project import ProjectVersion, StartupIdea
from app.schemas.score import BattleScore, ConfidenceScore
from app.schemas.agents import ScoutData, OpponentAnalystData, TreasuryAdvisorData, StrategyCommanderData, CriticAnalysisData, SWOTAnalysis, GTMStrategy
from app.llm.schemas import AgentLLMResponse

class GraphState(TypedDict):
    run_id: str
    project_id: str
    startup_idea: StartupIdea
    idea_version: ProjectVersion
    
    # Versioned Agent Outputs mapped to AgentLLMResponse Envelope
    commander_output: Optional[AgentLLMResponse[StrategyCommanderData]]
    scout_output: Optional[AgentLLMResponse[ScoutData]]
    analyst_output: Optional[AgentLLMResponse[OpponentAnalystData]]
    treasury_output: Optional[AgentLLMResponse[TreasuryAdvisorData]]
    critic_output: Optional[AgentLLMResponse[CriticAnalysisData]]
    swot_analysis: Optional[SWOTAnalysis]
    gtm_strategy: Optional[GTMStrategy]
    
    debate_records: Annotated[List[Any], operator.add]
    battle_score: Optional[BattleScore]
    battle_verdict: Optional[str]
    confidence_score: Optional[ConfidenceScore]
    final_report: Optional[Any]
    
    pivot_mandated: bool
    errors: Annotated[List[str], operator.add]
    execution_logs: Annotated[List[str], operator.add]

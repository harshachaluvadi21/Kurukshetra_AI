import operator
from typing import TypedDict, Annotated, List, Optional
from app.schemas.project import StartupIdea
from app.graph.debate_models import Vulnerability, Defense, DebateVerdict, DebateHistoryItem
from app.schemas.agents import OpponentAnalystData, TreasuryAdvisorData, ScoutData, CriticAnalysisData, SWOTAnalysis
from app.llm.schemas import AgentLLMResponse

class DebateState(TypedDict):
    run_id: str
    debate_id: str
    current_round: int
    max_rounds: int
    startup_idea: Optional[StartupIdea]
    
    # Inputs (Upgraded to LLM Envelope)
    analyst_output: Optional[AgentLLMResponse[OpponentAnalystData]]
    treasury_output: Optional[AgentLLMResponse[TreasuryAdvisorData]]
    scout_output: Optional[AgentLLMResponse[ScoutData]]
    critic_output: Optional[AgentLLMResponse[CriticAnalysisData]]
    swot_analysis: Optional[SWOTAnalysis]
    
    # Outputs
    vulnerabilities: Annotated[List[Vulnerability], operator.add]
    defenses: Annotated[List[Defense], operator.add]
    verdict: Optional[DebateVerdict]
    
    pivot_required: bool
    debate_history: Annotated[List[DebateHistoryItem], operator.add]

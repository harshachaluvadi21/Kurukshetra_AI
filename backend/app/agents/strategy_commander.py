import os
from typing import Dict, Any
from app.agents.base import BaseAgent
from app.graph.state import GraphState
from app.schemas.agents import StrategyCommanderData
from app.llm.schemas import AgentLLMResponse
from app.llm.router import llm_router

class StrategyCommander(BaseAgent):
    def __init__(self):
        super().__init__("Strategy Commander")

    def validate_input(self, state: GraphState) -> bool:
        return state.get("startup_idea") is not None

    def validate_output(self, output: Dict[str, Any]) -> bool:
        return "commander_output" in output

    async def _execute(self, state: GraphState) -> Dict[str, Any]:
        idea = state["startup_idea"]
        
        prompt_path = os.path.join(os.path.dirname(__file__), '..', 'llm', 'prompts', 'strategy_commander.txt')
        with open(prompt_path, 'r') as f:
            prompt_template = f.read()
        
        prompt = prompt_template.format(
            company_name=idea.company_name,
            business_concept=idea.business_concept,
            industry=idea.industry,
            problem_statement=idea.problem_statement or "Not provided",
            target_users=idea.target_users or "Not provided",
            revenue_model=idea.revenue_model or "Not provided"
        )
        
        run_id = state.get("run_id", "unknown")
        
        response = await llm_router.generate_structured(
            prompt=prompt,
            response_schema=AgentLLMResponse[StrategyCommanderData],
            run_id=run_id,
            agent_name=self.name
        )
        
        return {
            "commander_output": response
        }

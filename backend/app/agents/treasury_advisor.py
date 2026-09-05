import os
from typing import Dict, Any
from app.agents.base import BaseAgent
from app.graph.state import GraphState
from app.schemas.agents import TreasuryAdvisorData
from app.llm.schemas import AgentLLMResponse
from app.llm.router import llm_router

from app.services.market_context import detect_market_context

class TreasuryAdvisor(BaseAgent):
    def __init__(self):
        super().__init__("Treasury Advisor")

    def validate_input(self, state: GraphState) -> bool:
        return state.get("startup_idea") is not None

    def validate_output(self, output: Dict[str, Any]) -> bool:
        return "treasury_output" in output

    async def _execute(self, state: GraphState) -> Dict[str, Any]:
        idea = state["startup_idea"]
        market_ctx = detect_market_context(idea)
        
        prompt_path = os.path.join(os.path.dirname(__file__), '..', 'llm', 'prompts', 'treasury_advisor.txt')
        with open(prompt_path, 'r', encoding='utf-8') as f:
            prompt_template = f.read()
        
        prompt = prompt_template.format(
            target_market=market_ctx.country,
            currency_code=market_ctx.currency_code,
            currency_symbol=market_ctx.currency_symbol,
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
            response_schema=AgentLLMResponse[TreasuryAdvisorData],
            run_id=run_id,
            agent_name=self.name
        )
        
        # Ensure currency and currency_symbol are populated
        if not getattr(response.data, "currency", None):
            response.data.currency = market_ctx.currency_code
        if not getattr(response.data, "currency_symbol", None):
            response.data.currency_symbol = market_ctx.currency_symbol
        
        return {
            "treasury_output": response
        }

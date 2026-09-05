import json
import os
from typing import Any, Dict

from app.agents.base import BaseAgent
from app.graph.state import GraphState
from app.llm.router import llm_router
from app.llm.schemas import AgentLLMResponse
from app.schemas.agents import CriticAnalysisData


from app.services.market_context import detect_market_context

class CriticAgent(BaseAgent):
    def __init__(self):
        super().__init__("Critic Agent")

    def validate_input(self, state: GraphState) -> bool:
        return all([
            state.get("startup_idea"),
            state.get("scout_output"),
            state.get("analyst_output"),
            state.get("treasury_output"),
            state.get("swot_analysis"),
        ])

    def validate_output(self, output: Dict[str, Any]) -> bool:
        return "critic_output" in output

    async def _execute(self, state: GraphState) -> Dict[str, Any]:
        idea = state["startup_idea"]
        run_id = state.get("run_id", "unknown")
        market_ctx = detect_market_context(idea)

        prompt_path = os.path.join(os.path.dirname(__file__), "..", "llm", "prompts", "critic_agent.txt")
        with open(prompt_path, "r", encoding="utf-8") as f:
            prompt_template = f.read()

        prompt = prompt_template.format(
            target_market=market_ctx.country,
            currency_code=market_ctx.currency_code,
            currency_symbol=market_ctx.currency_symbol,
            company_name=idea.company_name,
            business_concept=idea.business_concept,
            problem_statement=idea.problem_statement or "Not provided",
            target_users=idea.target_users or "Not provided",
            revenue_model=idea.revenue_model or "Not provided",
            market_findings=json.dumps(state["scout_output"].data.model_dump(), indent=2, default=str),
            competitor_findings=json.dumps(state["analyst_output"].data.model_dump(), indent=2, default=str),
            financial_findings=json.dumps(state["treasury_output"].data.model_dump(), indent=2, default=str),
            swot_analysis=json.dumps(state["swot_analysis"].model_dump(), indent=2),
        )

        response = await llm_router.generate_structured(
            prompt=prompt,
            response_schema=AgentLLMResponse[CriticAnalysisData],
            run_id=run_id,
            agent_name=self.name,
        )

        return {"critic_output": response}

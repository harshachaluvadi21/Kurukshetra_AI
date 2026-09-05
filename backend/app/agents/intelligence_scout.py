import os
import json
from typing import Dict, Any
from app.agents.base import BaseAgent
from app.graph.state import GraphState
from app.schemas.agents import ScoutData
from app.llm.schemas import AgentLLMResponse
from app.llm.router import llm_router
from app.intelligence.service import intelligence_service
from app.rag.knowledge_service import knowledge_service
from app.intelligence.evidence_aggregator import evidence_aggregator

from app.services.market_context import detect_market_context

class IntelligenceScout(BaseAgent):
    def __init__(self):
        super().__init__("Intelligence Scout")

    def validate_input(self, state: GraphState) -> bool:
        return state.get("startup_idea") is not None

    def validate_output(self, output: Dict[str, Any]) -> bool:
        return "scout_output" in output

    async def _execute(self, state: GraphState) -> Dict[str, Any]:
        idea = state["startup_idea"]
        run_id = state.get("run_id", "unknown")
        market_ctx = detect_market_context(idea)
        
        # 1. Gather Web Intelligence with geography-aware query
        market_qualifier = f"in {market_ctx.country}" if market_ctx.country else ""
        query = f"{idea.business_concept} {market_qualifier} market size trends".strip()
        search_intel = await intelligence_service.gather_intelligence(
            query=query, 
            run_id=run_id, 
            agent_name=self.name,
            claim_context=f"Market sizing and macro trends for {market_ctx.country}"
        )
        
        # 2. Gather Knowledge Base Intelligence (RAG)
        knowledge_evidence = await knowledge_service.retrieve_knowledge(
            query=query,
            claim_context="Startup evaluation framework for market sizing",
            run_id=run_id,
            agent_name=self.name,
            k=3
        )
        
        # 3. Aggregate Evidence
        combined_pkg = evidence_aggregator.merge(
            search_evidence=[search_intel["evidence"]],
            knowledge_evidence=[knowledge_evidence],
            summary=f"Market sizing evidence combined from live search in {market_ctx.country} and curated frameworks."
        )
        citations = search_intel["citations"]
        
        # We serialize combined evidence to string to feed Gemini
        search_evidence_str = json.dumps(combined_pkg.model_dump(), indent=2)
        
        # 4. LLM Reasoning
        prompt_path = os.path.join(os.path.dirname(__file__), '..', 'llm', 'prompts', 'intelligence_scout.txt')
        with open(prompt_path, 'r', encoding='utf-8') as f:
            prompt_template = f.read()
        
        factors_str = "\n".join(f"- {f}" for f in market_ctx.relevant_factors) or "- Standard commercial regulations"
        
        prompt = prompt_template.format(
            target_market=market_ctx.country,
            currency_code=market_ctx.currency_code,
            currency_symbol=market_ctx.currency_symbol,
            market_factors=factors_str,
            company_name=idea.company_name,
            business_concept=idea.business_concept,
            industry=idea.industry,
            problem_statement=idea.problem_statement or "Not provided",
            target_users=idea.target_users or "Not provided",
            revenue_model=idea.revenue_model or "Not provided",
            search_evidence=search_evidence_str
        )
        
        response = await llm_router.generate_structured(
            prompt=prompt,
            response_schema=AgentLLMResponse[ScoutData],
            run_id=run_id,
            agent_name=self.name
        )
        
        # 5. Attach citations, currency, and combined evidence programmatically
        response.data.citations = citations
        response.data.evidence = combined_pkg
        if not getattr(response.data, "currency", None):
            response.data.currency = market_ctx.currency_code
        
        return {
            "scout_output": response
        }

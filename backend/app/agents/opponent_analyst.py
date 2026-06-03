import os
import json
from typing import Dict, Any
from app.agents.base import BaseAgent
from app.graph.state import GraphState
from app.schemas.agents import OpponentAnalystData
from app.llm.schemas import AgentLLMResponse
from app.llm.router import llm_router
from app.intelligence.service import intelligence_service
from app.rag.knowledge_service import knowledge_service
from app.intelligence.evidence_aggregator import evidence_aggregator

class OpponentAnalyst(BaseAgent):
    def __init__(self):
        super().__init__("Opponent Analyst")

    def validate_input(self, state: GraphState) -> bool:
        return state.get("startup_idea") is not None

    def validate_output(self, output: Dict[str, Any]) -> bool:
        return "analyst_output" in output

    async def _execute(self, state: GraphState) -> Dict[str, Any]:
        idea = state["startup_idea"]
        run_id = state.get("run_id", "unknown")
        
        # 1. Gather Web Intelligence
        query = f"{idea.business_concept} direct and indirect competitors"
        search_intel = await intelligence_service.gather_intelligence(
            query=query, 
            run_id=run_id, 
            agent_name=self.name,
            claim_context="Competitor discovery and market gaps"
        )
        
        # 2. Gather Knowledge Base Intelligence (RAG)
        knowledge_evidence = await knowledge_service.retrieve_knowledge(
            query=query,
            claim_context="Competitor analysis framework and moat evaluation",
            run_id=run_id,
            agent_name=self.name,
            k=3
        )
        
        # 3. Aggregate Evidence
        combined_pkg = evidence_aggregator.merge(
            search_evidence=[search_intel["evidence"]],
            knowledge_evidence=[knowledge_evidence],
            summary="Competitor evidence combined from live search and curated moat frameworks."
        )
        citations = search_intel["citations"]
        
        search_evidence_str = json.dumps(combined_pkg.model_dump(), indent=2)
        
        # 4. LLM Reasoning
        prompt_path = os.path.join(os.path.dirname(__file__), '..', 'llm', 'prompts', 'opponent_analyst.txt')
        with open(prompt_path, 'r') as f:
            prompt_template = f.read()
        
        prompt = prompt_template.format(
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
            response_schema=AgentLLMResponse[OpponentAnalystData],
            run_id=run_id,
            agent_name=self.name
        )
        
        # 5. Attach citations and combined evidence programmatically
        response.data.citations = citations
        response.data.evidence = combined_pkg
        
        return {
            "analyst_output": response
        }

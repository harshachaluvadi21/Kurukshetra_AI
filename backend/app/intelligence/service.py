import asyncio
from datetime import datetime
from typing import List, Dict, Any

from app.events.event_bus import event_bus
from app.events.event_types import AppEvent, EventType
from app.intelligence.models import SearchResult, Citation, SourceEvidence
from app.intelligence.providers.tavily_provider import TavilyProvider
from app.intelligence.providers.serper_provider import SerperProvider
from app.intelligence.providers.ranker import search_result_ranker

class IntelligenceService:
    def __init__(self):
        self.tavily = TavilyProvider()
        self.serper = SerperProvider()

    async def gather_intelligence(self, query: str, run_id: str, agent_name: str, claim_context: str) -> Dict[str, Any]:
        """
        Orchestrates gathering real intelligence from Tavily and Serper,
        ranks the results, generates citations, and packages evidence.
        """
        await self._emit(EventType.SEARCH_STARTED, run_id, agent_name, f"Initiating live intelligence gathering for: {query}")
        
        # 1. Fetch from Providers in parallel
        await self._emit(EventType.PROVIDER_REQUEST_STARTED, run_id, agent_name, "Requesting Tavily and Serper concurrently.")
        
        tavily_task = asyncio.create_task(self.tavily.search(query))
        serper_task = asyncio.create_task(self.serper.search(query))
        
        t_res, s_res = await asyncio.gather(tavily_task, serper_task)
        await self._emit(EventType.PROVIDER_RESPONSE_RECEIVED, run_id, agent_name, f"Received {len(t_res)} from Tavily, {len(s_res)} from Serper.")
        
        all_results = t_res + s_res
        
        # 2. Rank and Filter
        ranked_items = search_result_ranker.rank_and_filter(all_results)
        await self._emit(EventType.SEARCH_RESULTS_RANKED, run_id, agent_name, f"Ranked {len(ranked_items)} unique sources.")
        
        # 3. Generate Citations
        citations = []
        now = datetime.utcnow().isoformat()
        
        for item in ranked_items[:5]: # Take top 5
            r = item["result"]
            confidence = item["score"] / 100.0
            
            # Very basic heuristic to assign provider name
            provider = "tavily" if r in t_res else "serper"
            
            citations.append(Citation(
                title=r.title,
                url=r.url,
                source_type=r.source_type,
                confidence=confidence,
                retrieval_timestamp=now,
                provider=provider
            ))
            
        await self._emit(EventType.CITATIONS_GENERATED, run_id, agent_name, f"Generated {len(citations)} citations.", {"citations": [c.model_dump() for c in citations]})
        
        # 4. Package Evidence
        avg_conf = sum(c.confidence for c in citations) / len(citations) if citations else 0.0
        
        evidence = SourceEvidence(
            claim=claim_context,
            supporting_citations=citations,
            confidence=avg_conf
        )
        
        await self._emit(EventType.EVIDENCE_GENERATED, run_id, agent_name, "Packaged Live Evidence.")
        
        return {
            "evidence": evidence,
            "citations": citations
        }

    async def _emit(self, event_type: EventType, run_id: str, agent_name: str, message: str, payload: dict = None):
        event = AppEvent(
            event_type=event_type,
            run_id=run_id,
            timestamp=datetime.utcnow(),
            data={
                "agent_name": agent_name,
                "message": message,
                **(payload or {})
            }
        )
        await event_bus.publish(event)

intelligence_service = IntelligenceService()

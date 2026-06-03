import asyncio
from typing import List, Dict, Any
from datetime import datetime
from app.events.event_bus import event_bus
from app.events.event_types import AppEvent, EventType
from app.rag.vectorstore.chroma import ChromaVectorStore
from app.rag.models import KnowledgeChunk, KnowledgeEvidence

class KnowledgeService:
    def __init__(self):
        # Instantiate the vector store
        self.vector_store = ChromaVectorStore()

    async def retrieve_knowledge(self, query: str, claim_context: str, run_id: str, agent_name: str, k: int = 4) -> KnowledgeEvidence:
        """
        Retrieves relevant chunks from ChromaDB and packages them into KnowledgeEvidence.
        """
        await self._emit(EventType.RAG_RETRIEVAL_STARTED, run_id, agent_name, f"Retrieving knowledge for: {query}")
        
        try:
            # Langchain chroma similarity search
            # similarity_search_with_score returns (Document, score)
            results = self.vector_store.similarity_search_with_score(query, k=k)
            
            chunks = []
            for doc, score in results:
                # We handle L2 distance -> relevance score inversion if necessary, 
                # but for now we'll just normalize or use the raw score.
                relevance = max(0.0, 1.0 - score) if score < 1.0 else 0.5
                
                chunk = KnowledgeChunk(
                    chunk_id=doc.metadata.get("chunk_id", "unknown"),
                    source=doc.metadata.get("source", "unknown"),
                    document_name=doc.metadata.get("document_name", "unknown"),
                    category=doc.metadata.get("category", "unknown"),
                    content=doc.page_content,
                    relevance_score=relevance
                )
                chunks.append(chunk)

            await self._emit(EventType.CHUNKS_RETRIEVED, run_id, agent_name, f"Retrieved {len(chunks)} chunks from Knowledge Base.", {"chunks_count": len(chunks)})
            
            # Simple confidence calculation
            confidence = sum(c.relevance_score for c in chunks) / len(chunks) if chunks else 0.0
            
            evidence = KnowledgeEvidence(
                claim=claim_context,
                supporting_chunks=chunks,
                confidence=round(confidence, 2)
            )
            
            await self._emit(EventType.KNOWLEDGE_EVIDENCE_GENERATED, run_id, agent_name, f"Knowledge Evidence built with {evidence.confidence*100}% confidence.")
            return evidence
            
        except Exception as e:
            # If Google API key is missing or Chroma fails, fallback gracefully
            await self._emit(EventType.KNOWLEDGE_EVIDENCE_GENERATED, run_id, agent_name, f"Knowledge retrieval failed: {str(e)}")
            return KnowledgeEvidence(
                claim=claim_context,
                supporting_chunks=[],
                confidence=0.0
            )

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

knowledge_service = KnowledgeService()

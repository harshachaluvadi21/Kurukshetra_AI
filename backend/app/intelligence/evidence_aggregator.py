from typing import List
from app.intelligence.models import SourceEvidence
from app.rag.models import KnowledgeEvidence, CombinedEvidence

class EvidenceAggregator:
    def merge(self, search_evidence: List[SourceEvidence], knowledge_evidence: List[KnowledgeEvidence], summary: str = "") -> CombinedEvidence:
        """
        Merges external search evidence and internal knowledge evidence into a CombinedEvidence package.
        """
        # Calculate combined confidence
        total_confidence = 0.0
        count = 0
        
        for se in search_evidence:
            total_confidence += se.confidence
            count += 1
            
        for ke in knowledge_evidence:
            total_confidence += ke.confidence
            count += 1
            
        combined_confidence = round(total_confidence / count, 2) if count > 0 else 0.0
        
        return CombinedEvidence(
            search_evidence=search_evidence,
            knowledge_evidence=knowledge_evidence,
            combined_confidence=combined_confidence,
            summary=summary
        )

evidence_aggregator = EvidenceAggregator()

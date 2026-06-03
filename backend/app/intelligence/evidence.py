from typing import List
from app.intelligence.models import Citation, SourceEvidence

class EvidenceBuilder:
    def build_evidence(self, claim: str, citations: List[Citation]) -> SourceEvidence:
        """Aggregates citations into a SourceEvidence package."""
        if not citations:
            return SourceEvidence(claim=claim, supporting_citations=[], confidence=0.0)
            
        # Simple confidence aggregation for V1 (average of citation confidences)
        avg_confidence = sum(c.confidence for c in citations) / len(citations)
        
        return SourceEvidence(
            claim=claim,
            supporting_citations=citations,
            confidence=round(avg_confidence, 2)
        )

evidence_builder = EvidenceBuilder()

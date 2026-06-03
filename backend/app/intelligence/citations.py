from typing import List
from app.intelligence.models import SearchResult, Citation
from app.intelligence.source_validator import source_validator

class CitationGenerator:
    def generate(self, ranked_results: List[SearchResult]) -> List[Citation]:
        """Converts top ranked search results into structured Citations."""
        citations = []
        for res in ranked_results[:5]: # Take top 5
            score = source_validator.ranking_rules.get(res.source_type, 25)
            confidence = score / 100.0
            
            citations.append(Citation(
                title=res.title,
                url=res.url,
                source_type=res.source_type,
                confidence=confidence
            ))
        return citations

citation_generator = CitationGenerator()

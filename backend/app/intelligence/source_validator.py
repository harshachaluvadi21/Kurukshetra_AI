from typing import List
from app.intelligence.models import SearchResult

class SourceValidator:
    def __init__(self):
        # Deterministic Ranking Rules
        self.ranking_rules = {
            "Government Source": 95,
            "Research Report": 90,
            "Academic Paper": 90,
            "Established Publication": 85,
            "Company Website": 75,
            "Industry Blog": 50,
            "Unknown Source": 25
        }

    def rank_sources(self, results: List[SearchResult]) -> List[SearchResult]:
        """Ranks search results deterministically based on source type."""
        # We can add a temporary attribute or just sort
        def get_score(res: SearchResult) -> int:
            return self.ranking_rules.get(res.source_type, 25)
        
        # Sort descending by score
        return sorted(results, key=get_score, reverse=True)

source_validator = SourceValidator()

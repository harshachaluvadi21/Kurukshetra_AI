from typing import List, Dict, Any
from app.intelligence.models import SearchResult
from urllib.parse import urlparse

class SearchResultRanker:
    def rank_and_filter(self, results: List[SearchResult]) -> List[Dict[str, Any]]:
        """
        Deduplicates, scores, and ranks SearchResults based on deterministic domain authority rules.
        Returns a list of dicts with the original result, score, and ranking reason.
        """
        seen_urls = set()
        ranked = []
        
        for r in results:
            if r.url in seen_urls:
                continue
            seen_urls.add(r.url)
            
            domain = urlparse(r.url).netloc.lower()
            
            # Simple deterministic ranking rules
            if domain.endswith(".gov"):
                score = 95
                reason = "Government Source"
                source_type = "Government"
            elif domain.endswith(".edu"):
                score = 90
                reason = "Academic Source"
                source_type = "Academic"
            elif "mckinsey" in domain or "gartner" in domain or "forrester" in domain:
                score = 85
                reason = "Research Report"
                source_type = "Research"
            elif "forbes" in domain or "techcrunch" in domain or "wsj" in domain:
                score = 80
                reason = "Established Publication"
                source_type = "News"
            elif domain.count('.') == 1: # naive heuristic for main company sites
                score = 70
                reason = "Company Website"
                source_type = "Corporate"
            else:
                score = 50
                reason = "Blog / General"
                source_type = "Blog"
                
            r.source_type = source_type
            
            ranked.append({
                "result": r,
                "score": score,
                "reason": reason
            })
            
        # Sort descending by score
        ranked.sort(key=lambda x: x["score"], reverse=True)
        return ranked

search_result_ranker = SearchResultRanker()

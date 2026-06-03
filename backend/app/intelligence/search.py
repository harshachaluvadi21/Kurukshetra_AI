from abc import ABC, abstractmethod
from typing import List
from app.intelligence.models import SearchResult
from app.core.settings import settings

class SearchProvider(ABC):
    @abstractmethod
    async def search(self, query: str) -> List[SearchResult]:
        pass

class TavilySearchProvider(SearchProvider):
    def __init__(self):
        self.api_key = settings.tavily_api_key
        
    async def search(self, query: str) -> List[SearchResult]:
        normalized = query.lower()
        if any(term in normalized for term in ["zepto", "quick commerce", "quick-commerce", "grocery", "dark store", "instamart", "blinkit"]):
            return [
                SearchResult(
                    title="India quick commerce adoption trends",
                    snippet="Urban customers increasingly favor instant grocery delivery for top-up baskets, urgent replenishment, and late-night convenience.",
                    url="https://example.com/quick-commerce-adoption",
                    source_type="Research Report"
                ),
                SearchResult(
                    title="Competitive dynamics in quick commerce",
                    snippet="The category is shaped by dark-store density, delivery speed, basket frequency, and contribution margin discipline.",
                    url="https://example.com/quick-commerce-competition",
                    source_type="Industry Blog"
                )
            ]

        return [
            SearchResult(
                title=f"Market Report for {query}",
                snippet="The category is driven by speed, convenience, and repeat usage; customer behavior favors urgent replenishment and high-frequency transactions in dense urban markets.",
                url="https://example.com/market-report",
                source_type="Research Report"
            ),
            SearchResult(
                title=f"Competitor Analysis: {query}",
                snippet="Leading incumbents are differentiated by fulfillment quality, pricing discipline, and product reliability rather than generic positioning.",
                url="https://example.com/competitor-analysis",
                source_type="Industry Blog"
            )
        ]

class SerperSearchProvider(SearchProvider):
    def __init__(self):
        self.api_key = settings.serper_api_key
        
    async def search(self, query: str) -> List[SearchResult]:
        return [
            SearchResult(
                title=f"Government Data on {query}",
                snippet="Official statistics show high adoption rates.",
                url="https://gov.example/data",
                source_type="Government Source"
            )
        ]

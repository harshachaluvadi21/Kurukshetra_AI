from abc import ABC, abstractmethod
from typing import List
from app.intelligence.models import SearchResult

class SearchProvider(ABC):
    @abstractmethod
    async def search(self, query: str) -> List[SearchResult]:
        """Execute search against external API and return normalized SearchResult objects."""
        pass

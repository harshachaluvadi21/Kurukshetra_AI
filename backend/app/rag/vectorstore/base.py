from abc import ABC, abstractmethod
from typing import List, Dict, Any

class VectorStore(ABC):
    @abstractmethod
    def add_texts(self, texts: List[str], metadatas: List[Dict[str, Any]]):
        """Add texts to the vector store with associated metadata."""
        pass

    @abstractmethod
    def similarity_search_with_score(self, query: str, k: int = 4) -> List[tuple[Any, float]]:
        """Search the vector store and return results with relevance scores."""
        pass

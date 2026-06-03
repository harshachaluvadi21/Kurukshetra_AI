from abc import ABC, abstractmethod
from typing import TypeVar, Type, Any

T = TypeVar('T')

class LLMProvider(ABC):
    @abstractmethod
    async def generate_structured(
        self, 
        prompt: str, 
        response_schema: Type[T], 
        run_id: str, 
        agent_name: str
    ) -> T:
        """
        Generates a structured output matching the provided Pydantic schema.
        """
        pass

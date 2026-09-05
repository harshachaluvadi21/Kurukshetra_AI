import asyncio
from typing import TypeVar, Type
from datetime import datetime
from pydantic import BaseModel
from langchain_groq import ChatGroq
from app.llm.schemas import AgentLLMResponse
from app.core.settings import settings
from app.llm.base import LLMProvider

T = TypeVar('T', bound=BaseModel)

class GroqProvider(LLMProvider):
    def __init__(self, model_name: str = "llama-3.3-70b-versatile", max_retries: int = 1):
        api_key = settings.groq_api_key or "missing_key"
        self.model_name = model_name
        self.model = ChatGroq(model=model_name, temperature=0.2, groq_api_key=api_key)
        self.max_retries = max_retries

    async def generate_structured(
        self, 
        prompt: str, 
        response_schema: Type[AgentLLMResponse[T]], 
        run_id: str, 
        agent_name: str
    ) -> AgentLLMResponse[T]:
        structured_llm = self.model.with_structured_output(response_schema)
        
        for attempt in range(self.max_retries):
            try:
                start_time = datetime.utcnow()
                result = await structured_llm.ainvoke(prompt)
                latency = (datetime.utcnow() - start_time).total_seconds()
                
                # Append provider metadata via model_copy (Pydantic v2 safe)
                metadata = {
                    "provider": "groq",
                    "model": self.model_name,
                    "latency": round(latency, 2)
                }
                try:
                    result = result.model_copy(update={"provider_metadata": metadata})
                except Exception:
                    pass  # If model_copy fails, return result without metadata
                return result
            except Exception as e:
                if attempt < self.max_retries - 1:
                    await asyncio.sleep(1.0)
                else:
                    raise RuntimeError(f"GroqProvider ({self.model_name}) Error: {str(e)}")

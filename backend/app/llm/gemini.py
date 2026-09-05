import asyncio
from typing import TypeVar, Type
from datetime import datetime
from pydantic import BaseModel
from langchain_google_genai import ChatGoogleGenerativeAI
from app.events.event_bus import event_bus
from app.events.event_types import AppEvent, EventType
from app.llm.schemas import AgentLLMResponse
from app.core.settings import settings
from app.llm.base import LLMProvider

T = TypeVar('T', bound=BaseModel)

class GeminiProvider(LLMProvider):
    def __init__(self, model_name: str = "gemini-2.5-flash", max_retries: int = 1):
        api_key = settings.google_api_key or "missing_key_for_dev_mode"
        self.model_name = model_name
        self.model = ChatGoogleGenerativeAI(model=model_name, temperature=0.2, google_api_key=api_key)
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
                    "provider": "gemini",
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
                    raise RuntimeError(f"GeminiProvider Error: {str(e)}")

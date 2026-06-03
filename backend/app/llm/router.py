from typing import TypeVar, Type
from datetime import datetime
from pydantic import BaseModel
from app.events.event_bus import event_bus
from app.events.event_types import AppEvent, EventType
from app.llm.schemas import AgentLLMResponse
from app.llm.gemini import GeminiProvider
from app.llm.groq import GroqProvider

T = TypeVar('T', bound=BaseModel)

class LLMRouter:
    def __init__(self):
        self.gemini = GeminiProvider(model_name="gemini-2.5-flash", max_retries=1)
        self.groq_70b = GroqProvider(model_name="llama-3.3-70b-versatile", max_retries=1)
        self.groq_8b = GroqProvider(model_name="llama-3.1-8b-instant", max_retries=1)

    async def generate_structured(
        self, 
        prompt: str, 
        response_schema: Type[AgentLLMResponse[T]], 
        run_id: str, 
        agent_name: str
    ) -> AgentLLMResponse[T]:
        
        await self._emit(EventType.LLM_REQUEST_STARTED, run_id, agent_name, "Routing to Gemini")
        
        # 1. Attempt Gemini
        try:
            await self._emit(EventType.LLM_PROVIDER_SELECTED, run_id, agent_name, "Selected Gemini")
            result = await self.gemini.generate_structured(prompt, response_schema, run_id, agent_name)
            await self._emit(EventType.LLM_RESPONSE_RECEIVED, run_id, agent_name, "Gemini succeeded")
            return result
        except Exception as e:
            await self._emit(EventType.LLM_FALLBACK_TRIGGERED, run_id, agent_name, f"Gemini failed: {str(e)[:100]}. Falling back to Groq 70B")

        # 2. Attempt Groq 70B
        try:
            await self._emit(EventType.LLM_PROVIDER_SELECTED, run_id, agent_name, "Selected Groq 70B")
            result = await self.groq_70b.generate_structured(prompt, response_schema, run_id, agent_name)
            await self._emit(EventType.LLM_PROVIDER_RECOVERED, run_id, agent_name, "Groq 70B recovered successfully")
            return result
        except Exception as e:
            await self._emit(EventType.LLM_FALLBACK_TRIGGERED, run_id, agent_name, f"Groq 70B failed: {str(e)[:100]}. Falling back to Groq 8B")

        # 3. Attempt Groq 8B
        try:
            await self._emit(EventType.LLM_PROVIDER_SELECTED, run_id, agent_name, "Selected Groq 8B")
            result = await self.groq_8b.generate_structured(prompt, response_schema, run_id, agent_name)
            await self._emit(EventType.LLM_PROVIDER_RECOVERED, run_id, agent_name, "Groq 8B recovered successfully")
            return result
        except Exception as e:
            await self._emit(EventType.LLM_PROVIDER_FAILED, run_id, agent_name, f"All LLM Providers Exhausted. Last error: {str(e)}")
            raise RuntimeError(f"LLMRouter exhausted all providers. Last error: {str(e)}")

    async def _emit(self, event_type: EventType, run_id: str, agent_name: str, message: str):
        event = AppEvent(
            event_type=event_type,
            run_id=run_id,
            timestamp=datetime.utcnow(),
            data={"agent_name": agent_name, "message": message}
        )
        await event_bus.publish(event)

llm_router = LLMRouter()

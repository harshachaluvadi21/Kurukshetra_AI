import asyncio
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.llm.router import llm_router
from app.llm.schemas import AgentLLMResponse
from pydantic import BaseModel
from app.events.event_bus import event_bus
from app.events.event_types import AppEvent

class MockSchema(BaseModel):
    test_result: str

async def mock_subscriber(event: AppEvent):
    if "llm_" in event.event_type.value:
        print(f"[{event.event_type.value.upper()}] {event.data.get('message')}")

async def test_router():
    # Subscribe to see routing
    for event_type in [e for e in AppEvent.model_fields['event_type'].annotation]:
        event_bus.subscribe(event_type, mock_subscriber)

    print("\n--- Testing Gemini Success ---")
    try:
        res = await llm_router.generate_structured(
            prompt="Reply strictly with {'test_result': 'hello'}",
            response_schema=AgentLLMResponse[MockSchema],
            run_id="test-1",
            agent_name="TestAgent"
        )
        print(f"Result Provider: {res.provider_metadata}")
        print("PASS")
    except Exception as e:
        print(f"FAIL: {e}")

    print("\n--- Testing Gemini Failure -> Groq 70B Fallback ---")
    # Sabotage Gemini API key temporarily to force fallback
    original_gemini = llm_router.gemini.model
    try:
        from langchain_google_genai import ChatGoogleGenerativeAI
        llm_router.gemini.model = ChatGoogleGenerativeAI(model="gemini-2.5-flash", google_api_key="INVALID_KEY_TO_FORCE_403")
        res2 = await llm_router.generate_structured(
            prompt="Reply strictly with {'test_result': 'hello fallback'}",
            response_schema=AgentLLMResponse[MockSchema],
            run_id="test-2",
            agent_name="TestAgent"
        )
        print(f"Result Provider: {res2.provider_metadata}")
        print("PASS")
    except Exception as e:
        print(f"FAIL: {e}")
    finally:
        llm_router.gemini.model = original_gemini

if __name__ == "__main__":
    asyncio.run(test_router())

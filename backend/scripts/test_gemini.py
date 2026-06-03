import asyncio
import sys
import os
import time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.llm.gemini import gemini_service
from pydantic import BaseModel

class TestSchema(BaseModel):
    message: str
    confidence: float

async def test_gemini():
    print("==========================================================")
    print(" GEMINI VALIDATION ")
    print("==========================================================")
    
    start_time = time.time()
    try:
        response = await gemini_service.generate_structured(
            prompt="Write a short welcoming message for a startup founder. Set confidence to 0.95.",
            response_schema=TestSchema,
            run_id="test-run",
            agent_name="System"
        )
        latency = time.time() - start_time
        
        print("PASS")
        print(f"Latency: {latency:.2f}s")
        print(f"Response Sample: {response.data.message}")
        print(f"Validation Result: Confidence = {response.data.confidence}")
    except Exception as e:
        print("FAIL")
        print(f"Error Details: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(test_gemini())

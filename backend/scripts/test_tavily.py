import asyncio
import sys
import os
import time
import httpx

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.core.settings import settings

async def test_tavily():
    print("==========================================================")
    print(" TAVILY VALIDATION ")
    print("==========================================================")
    
    start_time = time.time()
    try:
        async with httpx.AsyncClient() as client:
            payload = {
                "api_key": settings.tavily_api_key,
                "query": "Recent AI startups 2026",
                "search_depth": "basic",
                "include_answer": False,
                "max_results": 3
            }
            
            response = await client.post("https://api.tavily.com/search", json=payload, timeout=10.0)
            response.raise_for_status()
            data = response.json()
            
            latency = time.time() - start_time
            results = data.get("results", [])
            
            print("PASS")
            print(f"Latency: {latency:.2f}s")
            print(f"Results Count: {len(results)}")
            if results:
                print(f"Sample Result Title: {results[0].get('title')}")
                
    except Exception as e:
        print("FAIL")
        print(f"Error Details: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(test_tavily())

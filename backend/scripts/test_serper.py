import asyncio
import sys
import os
import time
import httpx

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.core.settings import settings

async def test_serper():
    print("==========================================================")
    print(" SERPER VALIDATION ")
    print("==========================================================")
    
    start_time = time.time()
    try:
        async with httpx.AsyncClient() as client:
            headers = {
                "X-API-KEY": settings.serper_api_key,
                "Content-Type": "application/json"
            }
            payload = {
                "q": "Recent AI startups 2026",
                "num": 3
            }
            
            response = await client.post("https://google.serper.dev/search", headers=headers, json=payload, timeout=10.0)
            response.raise_for_status()
            data = response.json()
            
            latency = time.time() - start_time
            organic = data.get("organic", [])
            
            print("PASS")
            print(f"Latency: {latency:.2f}s")
            print(f"Results Count: {len(organic)}")
            if organic:
                print(f"Sample Result Title: {organic[0].get('title')}")
                
    except Exception as e:
        print("FAIL")
        print(f"Error Details: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(test_serper())

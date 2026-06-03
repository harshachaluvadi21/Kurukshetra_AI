import asyncio
import sys
import os
import time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.core.settings import settings
import chromadb

def test_chroma():
    print("==========================================================")
    print(" CHROMADB (REMOTE) VALIDATION ")
    print("==========================================================")
    
    start_time = time.time()
    try:
        if settings.chroma_host and settings.chroma_api_key:
            client = chromadb.HttpClient(
                host=settings.chroma_host,
                ssl=True,
                headers={"x-chroma-token": settings.chroma_api_key},
                tenant=settings.chroma_tenant or chromadb.config.DEFAULT_TENANT,
                database=settings.chroma_database or chromadb.config.DEFAULT_DATABASE
            )
        else:
            print("WARNING: Remote Chroma configs missing, falling back to local.")
            client = chromadb.PersistentClient(path=settings.chroma_persist_directory)
            
        heartbeat = client.heartbeat()
        latency = time.time() - start_time
        
        print("PASS")
        print(f"Latency: {latency:.2f}s")
        print(f"Heartbeat: {heartbeat}")
        
    except Exception as e:
        print("FAIL")
        print(f"Error Details: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    test_chroma()

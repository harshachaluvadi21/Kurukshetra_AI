import asyncio
import sys
import os
import time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.rag.knowledge_service import knowledge_service

async def test_rag():
    print("==========================================================")
    print(" RAG RETRIEVAL VALIDATION ")
    print("==========================================================")
    
    start_time = time.time()
    try:
        evidence = await knowledge_service.retrieve_knowledge(
            query="MVP and market sizing",
            claim_context="Testing retrieval logic",
            run_id="test-run",
            agent_name="System",
            k=2
        )
        
        latency = time.time() - start_time
        chunks = evidence.supporting_chunks
        
        print("PASS")
        print(f"Latency: {latency:.2f}s")
        print(f"Retrieved Chunks: {len(chunks)}")
        print(f"Confidence Score: {evidence.confidence}")
        
        if chunks:
            print(f"Top Chunk Content: {chunks[0].content[:100]}...")
            print(f"Top Chunk Metadata: {chunks[0].source} - {chunks[0].category}")
            
    except Exception as e:
        print("FAIL")
        print(f"Error Details: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(test_rag())

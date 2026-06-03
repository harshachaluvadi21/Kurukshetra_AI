import sys
import os
import time
from langsmith import Client

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.core.settings import settings

def test_langsmith():
    print("==========================================================")
    print(" LANGSMITH TRACING VALIDATION ")
    print("==========================================================")
    
    start_time = time.time()
    try:
        # Initialize client with settings or env
        os.environ["LANGCHAIN_API_KEY"] = settings.langchain_api_key or ""
        os.environ["LANGCHAIN_TRACING_V2"] = settings.langchain_tracing_v2 or "false"
        
        client = Client()
        projects = list(client.list_projects(limit=1))
        
        latency = time.time() - start_time
        
        print("PASS")
        print(f"Latency: {latency:.2f}s")
        print(f"LangSmith Project ID Found: {projects[0].id if projects else 'No previous projects, but auth passed.'}")
        
    except Exception as e:
        print("FAIL")
        print(f"Error Details: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    test_langsmith()

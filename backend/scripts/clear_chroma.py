import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.core.settings import settings
import chromadb

def clear_chroma():
    print("Connecting to ChromaDB...")
    if settings.chroma_host and settings.chroma_api_key:
        client = chromadb.HttpClient(
            host=settings.chroma_host,
            ssl=True,
            headers={"x-chroma-token": settings.chroma_api_key},
            tenant=settings.chroma_tenant or chromadb.config.DEFAULT_TENANT,
            database=settings.chroma_database or chromadb.config.DEFAULT_DATABASE
        )
    else:
        client = chromadb.PersistentClient(path=settings.chroma_persist_directory)

    collection_name = "kurukshetra_knowledge"
    
    try:
        client.delete_collection(name=collection_name)
        print(f"Collection '{collection_name}' deleted successfully.")
    except Exception as e:
        print(f"Error deleting collection: {e}")

if __name__ == "__main__":
    clear_chroma()

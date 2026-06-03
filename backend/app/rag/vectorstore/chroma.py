from typing import List, Dict, Any
from app.rag.vectorstore.base import VectorStore
from app.core.settings import settings

import chromadb
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings

class ChromaVectorStore(VectorStore):
    def __init__(self, collection_name: str = "kurukshetra_knowledge"):
        self.persist_directory = settings.chroma_persist_directory
        
        if settings.chroma_host and settings.chroma_api_key:
            self.client = chromadb.HttpClient(
                host=settings.chroma_host,
                ssl=True,
                headers={"x-chroma-token": settings.chroma_api_key},
                tenant=settings.chroma_tenant or chromadb.config.DEFAULT_TENANT,
                database=settings.chroma_database or chromadb.config.DEFAULT_DATABASE
            )
        else:
            self.client = chromadb.PersistentClient(path=self.persist_directory)
        
        # We assume Google API key is available in settings or environment
        api_key = settings.google_api_key or "dummy_key_for_dev_mode"
        self.embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-2", google_api_key=api_key)
        
        self.vector_store = Chroma(
            client=self.client,
            collection_name=collection_name,
            embedding_function=self.embeddings,
        )

    def add_texts(self, texts: List[str], metadatas: List[Dict[str, Any]]):
        self.vector_store.add_texts(texts=texts, metadatas=metadatas)

    def similarity_search_with_score(self, query: str, k: int = 4) -> List[tuple[Any, float]]:
        # In langchain_chroma, similarity_search_with_score returns (Document, score)
        return self.vector_store.similarity_search_with_score(query=query, k=k)

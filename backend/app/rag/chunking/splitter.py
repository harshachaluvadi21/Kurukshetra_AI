import uuid
from typing import List
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

class ChunkingPipeline:
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            add_start_index=True,
        )

    def split_document(self, text: str, source: str, document_name: str, category: str) -> List[Document]:
        """
        Splits text into chunks while preserving required metadata.
        """
        docs = self.splitter.create_documents(
            texts=[text],
            metadatas=[{
                "source": source,
                "document_name": document_name,
                "category": category,
            }]
        )
        
        # Add chunk_id to each document's metadata
        for doc in docs:
            doc.metadata["chunk_id"] = str(uuid.uuid4())
            
        return docs

chunking_pipeline = ChunkingPipeline()

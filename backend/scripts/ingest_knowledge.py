import sys
import os
import glob

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.rag.chunking.splitter import chunking_pipeline
from app.rag.vectorstore.chroma import ChromaVectorStore

def ingest_all():
    print("==========================================================")
    print(" INGESTING KNOWLEDGE BASE INTO CHROMADB ")
    print("==========================================================")
    
    # Initialize VectorStore
    vector_store = ChromaVectorStore()
    
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'knowledge_base'))
    
    # Supported categories
    categories = ["startup_frameworks", "vc_frameworks", "product_strategy", "market_research", "gtm_playbooks"]
    
    total_chunks = 0
    
    for category in categories:
        cat_path = os.path.join(base_dir, category)
        if not os.path.exists(cat_path):
            continue
            
        txt_files = glob.glob(os.path.join(cat_path, "*.txt"))
        for filepath in txt_files:
            filename = os.path.basename(filepath)
            print(f"\nProcessing [{category}] {filename}...")
            
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                
            docs = chunking_pipeline.split_document(
                text=content,
                source=filepath,
                document_name=filename,
                category=category
            )
            
            texts = [doc.page_content for doc in docs]
            metadatas = [doc.metadata for doc in docs]
            
            vector_store.add_texts(texts=texts, metadatas=metadatas)
            
            print(f"  -> Added {len(docs)} chunks to ChromaDB.")
            total_chunks += len(docs)
            
    print(f"\nTotal Chunks Ingested: {total_chunks}")
    print("Ingestion Complete.")

if __name__ == "__main__":
    ingest_all()

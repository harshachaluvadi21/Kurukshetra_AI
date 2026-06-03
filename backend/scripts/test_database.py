import asyncio
import sys
import os
import time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.core.settings import settings
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text

async def test_database():
    print("==========================================================")
    print(" POSTGRESQL (NEON) VALIDATION ")
    print("==========================================================")
    
    start_time = time.time()
    try:
        # We need an asyncpg connection string. The neon DB url might be postgresql:// instead of postgresql+asyncpg://
        db_url = settings.database_url
        if db_url.startswith("postgresql://"):
            db_url = db_url.replace("postgresql://", "postgresql+asyncpg://", 1)
        if "sslmode=require" in db_url:
            db_url = db_url.replace("sslmode=require", "ssl=require")

        engine = create_async_engine(db_url, echo=False)
        
        async with engine.connect() as conn:
            result = await conn.execute(text("SELECT version();"))
            version_str = result.scalar()
            
        latency = time.time() - start_time
        
        print("PASS")
        print(f"Latency: {latency:.2f}s")
        print(f"Database Version: {version_str}")
        
    except Exception as e:
        print("FAIL")
        print(f"Error Details: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(test_database())

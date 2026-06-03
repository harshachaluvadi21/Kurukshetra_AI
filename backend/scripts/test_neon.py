import asyncio
from sqlalchemy import text
from app.db.database import AsyncSessionLocal

async def test_connection():
    try:
        async with AsyncSessionLocal() as session:
            result = await session.execute(text("SELECT version();"))
            version = result.scalar()
            print("Successfully connected to Neon PostgreSQL!")
            print("Version:", version)
    except Exception as e:
        print("Connection failed:", e)

if __name__ == "__main__":
    asyncio.run(test_connection())

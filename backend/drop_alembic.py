import asyncio
import os
from dotenv import load_dotenv
import asyncpg

load_dotenv()

async def main():
    url = os.environ['DATABASE_URL'].replace('+asyncpg', '')
    conn = await asyncpg.connect(url)
    await conn.execute('DROP TABLE IF EXISTS alembic_version CASCADE;')
    await conn.close()
    print('Dropped alembic_version')

asyncio.run(main())

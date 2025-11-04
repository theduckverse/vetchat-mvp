
import os
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

def _db_url():
    url = os.getenv("DATABASE_URL")
    if url:
        # Expect sync driver; convert to async where possible
        if url.startswith("postgresql://"):
            url = url.replace("postgresql://", "postgresql+psycopg2://")
        return url
    # Default to local SQLite (async)
    return "sqlite+aiosqlite:///./local.db"

ASYNC_DB_URL = _db_url().replace("+psycopg2", "+asyncpg") if "postgresql" in _db_url() else _db_url()

engine = create_async_engine(ASYNC_DB_URL, echo=False, future=True)
AsyncSessionLocal = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

async def get_session() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session

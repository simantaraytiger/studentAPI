from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite+aiosqlite:///./students.db"

# Create async engine
engine = create_async_engine(
    DATABASE_URL,
    echo=True,  # Optional: Logs SQL queries to console
    future=True,
)

# Create sessionmaker using AsyncSession
AsyncSessionLocal = sessionmaker(
    bind=engine, # type: ignore
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
) # type: ignore

# Base class for ORM models
Base = declarative_base()

# Dependency for FastAPI routes
async def get_async_db():
    async with AsyncSessionLocal() as session: # type: ignore
        try:
            yield session
        finally:
            await session.close()

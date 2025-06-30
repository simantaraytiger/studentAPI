from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite+aiosqlite:///./database.db"

engine = create_async_engine(
    DATABASE_URL,
    echo=True,
    future=True,
)

AsyncSessionLocal = sessionmaker(
    bind=engine, # type: ignore
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
) # type: ignore

Base = declarative_base()

async def get_async_db():
    async with AsyncSessionLocal() as session: # type: ignore
        try:
            yield session
        finally:
            await session.close()

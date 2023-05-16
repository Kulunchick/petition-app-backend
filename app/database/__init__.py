from typing import AsyncIterator

from sqlalchemy import URL
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from app.config import settings

ENGINE = create_async_engine(
    URL.create(
        "postgresql+asyncpg",
        username=settings.POSTGRES_USER,
        password=settings.POSTGRES_PASSWORD.get_secret_value(),
        host=settings.POSTGRES_HOST,
        port=settings.POSTGRES_PORT,
        database=settings.POSTGRES_DB,
    ),
    pool_pre_ping=True
)
ASYNC_SESSIONMAKER = async_sessionmaker(ENGINE)


async def get_session() -> AsyncIterator[AsyncSession]:
    async with ASYNC_SESSIONMAKER() as session:
        async with session.begin():
            yield session

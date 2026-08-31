from typing import AsyncGenerator
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from app.core.config import settings


def prepare_database_url(url: str):
    """
    Prepare the database URL for SQLAlchemy + asyncpg.

    asyncpg uses `ssl`, not `sslmode`.
    This converts sslmode=require to ssl=require.
    """

    parts = urlsplit(url)

    query_params = dict(parse_qsl(parts.query))

    connect_args = {}

    # Convert PostgreSQL/psycopg-style sslmode to asyncpg's ssl parameter.
    if "sslmode" in query_params:
        sslmode = query_params.pop("sslmode")

        if sslmode == "require":
            connect_args["ssl"] = "require"
        elif sslmode == "disable":
            connect_args["ssl"] = False
        else:
            connect_args["ssl"] = sslmode

    # If the URL already contains ?ssl=require, asyncpg can use it directly.
    new_query = urlencode(query_params)

    cleaned_url = urlunsplit(
        (
            parts.scheme,
            parts.netloc,
            parts.path,
            new_query,
            parts.fragment,
        )
    )

    return cleaned_url, connect_args


database_url, connect_args = prepare_database_url(settings.database_url)

engine = create_async_engine(
    database_url,
    echo=False,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
    connect_args=connect_args,
)

AsyncSessionLocal = async_sessionmaker(
    engine,
    expire_on_commit=False,
    class_=AsyncSession,
)


class Base(DeclarativeBase):
    pass


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


async def init_models() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

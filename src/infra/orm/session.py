from collections.abc import AsyncIterator, Callable
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)


type SessionFactory = Callable[[], AsyncSession]


def make_engine(
    url: str,
    *,
    echo: bool = False,
    pool_size: int = 20,
) -> AsyncEngine:
    return create_async_engine(
        url,
        echo=echo,
        pool_size=pool_size,
        future=True,
    )


def make_async_session_factory(engine: AsyncEngine) -> SessionFactory:
    return async_sessionmaker(
        bind=engine,
        autoflush=False,
        expire_on_commit=False,
        class_=AsyncSession,
    )


@asynccontextmanager
async def async_session(session_factory: SessionFactory) -> AsyncIterator[AsyncSession]:
    session = session_factory()

    try:
        yield session
        await session.commit()
    except:
        await session.rollback()
        raise
    finally:
        await session.close()

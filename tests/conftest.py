from collections.abc import AsyncIterator

import pytest
import pytest_asyncio
from asgi_lifespan import LifespanManager
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncEngine

from src.infra.config import Settings
from src.infra.orm.models.base import Base
from src.infra.orm.session import SessionFactory, make_async_session_factory, make_engine

from src.application.uow import SqlAlchemyUoW, UnitOfWork

from src.presentation.main import app

from tests.utils import create_database, drop_database


@pytest.fixture(scope="session")
def conf() -> Settings:
    settings = Settings()
    return settings


@pytest.fixture(scope="session")
def db_url(conf) -> str:
    return f"{conf.database_url}_test"


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="session")
def base_url() -> str:
    return "http://test"


@pytest_asyncio.fixture
async def client(base_url: str) -> AsyncIterator[AsyncClient]:
    async with LifespanManager(app):
        transport = ASGITransport(app)
        async with AsyncClient(transport=transport, base_url=base_url) as async_client:
            yield async_client


@pytest.fixture
def password() -> str:
    """Valid password for registration."""
    return "Test123!"


@pytest_asyncio.fixture(loop_scope="session")
async def database(db_url):
    await create_database(db_url)

    engine = make_engine(db_url)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    try:
        yield db_url
    finally:
        # async with engine.begin() as conn:
        #     await conn.run_sync(Base.metadata.drop_all)
        await drop_database(db_url)


@pytest_asyncio.fixture(scope="session", autouse=True)
async def engine(db_url: str):
    engine = make_engine(db_url)
    try:
        yield engine

    finally:
        await engine.dispose()


@pytest_asyncio.fixture(scope="session", autouse=True)
async def db_session_factory(engine: AsyncEngine) -> SessionFactory:
    return make_async_session_factory(engine)


@pytest_asyncio.fixture
async def uow(db_session_factory: SessionFactory, database) -> UnitOfWork:
    return SqlAlchemyUoW(db_session_factory)

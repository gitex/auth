import asyncio
from collections.abc import AsyncIterator

import pytest
import pytest_asyncio
from asgi_lifespan import LifespanManager
from httpx import ASGITransport, AsyncClient

from src.infra.config import Settings, settings
from src.infra.orm.models.base import Base
from src.infra.orm.session import make_engine

from src.bootstrap.login import AuthContainer

from src.presentation.main import app, container as main_container

from tests.utils import create_database


@pytest.fixture(scope="session", autouse=True)
def conf() -> Settings:
    """Test settings"""
    settings.database_url = f"{settings.database_url}_test"
    settings.debug = True
    return settings


@pytest.fixture(scope="session")
def db_url(conf: Settings) -> str:
    """alias"""
    return conf.database_url


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def base_url() -> str:
    return "http://test"


@pytest_asyncio.fixture
async def client(base_url: str) -> AsyncIterator[AsyncClient]:
    async with LifespanManager(app):
        transport = ASGITransport(app)
        async with AsyncClient(transport=transport, base_url=base_url) as async_client:
            yield async_client


@pytest.fixture(scope="session", autouse=True)
def container(conf: Settings) -> AuthContainer:
    """Required for database_url update"""
    main_container.config.from_pydantic(conf)
    return main_container


@pytest.fixture(scope="session")
def password() -> str:
    """Valid password for registration."""
    return "Test123!"


@pytest_asyncio.fixture(scope="session", loop_scope="session", autouse=True)
async def database(db_url: str, event_loop):
    """Test database controller."""

    await create_database(db_url)

    engine = make_engine(db_url)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    try:
        yield
    finally:
        # async with engine.begin() as conn:
        #     await conn.run_sync(Base.metadata.drop_all)
        # await drop_database(db_url)
        pass


# @pytest_asyncio.fixture
# async def async_engine(db_url: str, database):
#     engine = make_engine(db_url)
#     try:
#         yield engine
#     finally:
#         await engine.dispose()
#

# @pytest.fixture
# def db_session_factory(async_engine: AsyncEngine) -> SessionFactory:
#     return make_async_session_factory(async_engine)


# @pytest_asyncio.fixture
# async def uow(db_session_factory: SessionFactory):
# async with SqlAlchemyUoW(db_session_factory) as uow:
# yield uow
@pytest_asyncio.fixture
async def uow(container: AuthContainer):
    async with container.uow() as uow:
        yield uow

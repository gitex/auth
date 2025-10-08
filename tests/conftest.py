import os
from collections.abc import AsyncGenerator, AsyncIterator

import pytest
import pytest_asyncio
from asgi_lifespan import LifespanManager
from faker import Faker
from httpx import ASGITransport, AsyncClient
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from src.domain.entities import Account
from src.domain.value_objects import Email, Password

from src.infra.config import Settings, settings
from src.infra.orm.models.base import Base
from src.infra.orm.session import make_engine

from src.application.register.service import RegisterCommand

from src.bootstrap.login import AuthContainer

from src.presentation.main import app, container as main_container

from tests.utils import create_database


@pytest.fixture(scope="session")
def worker_id() -> str:
    return os.environ.get("PYTEST_XDIST_WORKER", "gw0")


@pytest.fixture(scope="session", autouse=True)
def conf(worker_id: str) -> Settings:
    """Test settings"""
    settings.database_url = f"{settings.database_url}_test_{worker_id}"
    settings.debug = True
    return settings


@pytest.fixture(scope="session")
def db_url(conf: Settings) -> str:
    """alias"""
    return conf.database_url


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


# @pytest.fixture(scope="session", autouse=True)
# def event_loop() -> Generator[AbstractEventLoop]:
#     loop = asyncio.new_event_loop()
#     yield loop
#     loop.close()


@pytest.fixture(scope="session")
def base_url() -> str:
    return "http://test"


@pytest_asyncio.fixture
async def client(container: AuthContainer, base_url: str) -> AsyncIterator[AsyncClient]:
    async with LifespanManager(app):
        transport = ASGITransport(app)
        async with AsyncClient(transport=transport, base_url=base_url) as async_client:
            yield async_client


@pytest_asyncio.fixture(scope="session")
async def async_engine(db_url: str, database: str) -> AsyncGenerator[AsyncEngine]:
    engine = create_async_engine(db_url, echo=False, poolclass=NullPool)
    try:
        yield engine
    finally:
        await engine.dispose()


# @pytest.fixture
@pytest.fixture(scope="session", autouse=True)
def container(conf: Settings, async_engine: AsyncEngine) -> AuthContainer:
    """Required for database_url update"""
    main_container.config.from_pydantic(conf)
    main_container.engine.override(async_engine)
    return main_container


@pytest.fixture(scope="session")
def password() -> str:
    """Valid password for registration."""
    return "Test123!"


@pytest_asyncio.fixture(scope="session", autouse=True)
async def database(db_url: str):
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


@pytest.fixture(scope="session")
def faker() -> Faker:
    return Faker()


@pytest_asyncio.fixture
async def account(password: str, container: AuthContainer, faker: Faker) -> Account:
    register_service = container.register_service()
    result = await register_service.register(
        RegisterCommand(
            email=Email(faker.email()),
            password=Password(password),
        )
    )
    return result.account

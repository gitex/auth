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

from src.application import RegisterCommand, UnitOfWork

from src.bootstrap import AuthContainer

from src.presentation.main import app, container as main_container

from tests.utils import create_database, drop_database


@pytest.fixture(scope='session')
def worker_id() -> str:
    """Worker ID of pytest-xdist."""
    return os.environ.get('PYTEST_XDIST_WORKER', 'gw0')


@pytest.fixture(scope='session', autouse=True)
def conf(worker_id: str) -> Settings:
    """Change settings for tests.

    Do not push too far: settings must be as close as possible to real conditions.
    """
    settings.database_url = f'{settings.database_url}_test_{worker_id}'
    settings.debug = True
    return settings


@pytest.fixture(scope='session')
def db_url(conf: Settings) -> str:
    """Alias for database_url."""
    return conf.database_url


@pytest.fixture(scope='session')
def anyio_backend() -> str:
    """Mode for pytest-asyncio."""
    return 'asyncio'


@pytest.fixture(scope='session')
def base_url() -> str:
    """Base url for httpx."""
    return 'http://test'


@pytest_asyncio.fixture
async def client(container: AuthContainer, base_url: str) -> AsyncIterator[AsyncClient]:
    """HTTP client."""
    async with LifespanManager(app):
        transport = ASGITransport(app)
        async with AsyncClient(transport=transport, base_url=base_url) as async_client:
            yield async_client


@pytest_asyncio.fixture(scope='session')
async def async_engine(db_url: str, database: str) -> AsyncGenerator[AsyncEngine]:
    """Special async engine for tests.

    Hard to run default async_engine without NullPool.
    """
    engine = create_async_engine(db_url, echo=False, poolclass=NullPool)
    try:
        yield engine
    finally:
        await engine.dispose()


@pytest.fixture(scope='session', autouse=True)
def container(conf: Settings, async_engine: AsyncEngine) -> AuthContainer:
    """Main DI container.

    Idea: pre-build some dependencies before run HTTP client.
    """
    main_container.config.from_pydantic(conf)
    main_container.engine.override(async_engine)
    return main_container


@pytest.fixture
def email(faker: Faker) -> str:
    return faker.email()


@pytest.fixture
def password(faker: Faker) -> str:
    """Valid password for registration."""
    return faker.password(
        length=10,
        digits=True,
        lower_case=True,
        upper_case=True,
        special_chars=True,
    )


@pytest_asyncio.fixture(scope='session', autouse=True)
async def database(db_url: str) -> AsyncGenerator[None]:
    """Test database controller."""
    await create_database(db_url)

    engine = make_engine(db_url)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    try:
        yield
    finally:
        await drop_database(db_url)


@pytest_asyncio.fixture
async def uow(container: AuthContainer) -> AsyncGenerator[UnitOfWork]:
    """Unit of Work from container.

    Main idea is build services close as possible to real conditions.
    """
    async with container.uow() as uow:
        yield uow


@pytest.fixture(scope='session')
def faker() -> Faker:
    """Just a Faker as fixture."""
    return Faker()


@pytest_asyncio.fixture
async def account(password: str, container: AuthContainer, faker: Faker) -> Account:
    """Account factory.

    Again: as close as possible to real conditions.
    """
    register_service = container.register_service()
    result = await register_service.register(
        RegisterCommand(
            email=Email(faker.email()),
            password=Password(password),
        ),
    )
    return result.account

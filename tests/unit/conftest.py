from uuid import uuid4

import pytest
from faker import Faker

from src.domain.factories.claims import ClaimsFactory

from src.bootstrap.wiring import AuthContainer


@pytest.fixture(scope='session')
def ts(faker: Faker) -> int:
    """Just random timestamp."""
    return int(faker.unix_time())


@pytest.fixture
def sub() -> str:
    """Random claims.sub."""
    return uuid4().hex


@pytest.fixture
def claims_factory(container: AuthContainer) -> ClaimsFactory:
    return container.claims_factory()

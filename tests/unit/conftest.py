from uuid import uuid4

import pytest
from faker import Faker

from src.infra.claims import Claims, ClaimsFactory
from src.infra.claims.policies import TokenPolicy
from src.infra.claims.value_objects import Timestamp


@pytest.fixture(scope='session')
def ts(faker: Faker) -> Timestamp:
    """Just random timestamp."""
    return Timestamp(int(faker.unix_time()))


@pytest.fixture
def sub() -> str:
    """Random claims.sub."""
    return uuid4().hex


@pytest.fixture
def token_policy() -> TokenPolicy:
    """Token policy factory."""
    return TokenPolicy(
        issuer='test',
        audience='test',
    )


@pytest.fixture
def claims_factory(token_policy: TokenPolicy) -> ClaimsFactory:
    """Claims factory."""
    return ClaimsFactory(token_policy)


@pytest.fixture
def refresh_claims(claims_factory: ClaimsFactory, sub: str) -> Claims:
    """Refresh claims factory."""
    return claims_factory.refresh_claims(sub)


@pytest.fixture
def access_claims(claims_factory: ClaimsFactory, sub: str) -> Claims:
    """Access claims factory."""
    return claims_factory.access_claims(sub)

from uuid import uuid4

import pytest

from src.infra.claims import Claims, ClaimsFactory
from src.infra.claims.policies import TokenPolicy


@pytest.fixture(scope="session")
def ts() -> int:
    return 1759420090


@pytest.fixture
def sub() -> str:
    return uuid4().hex


@pytest.fixture
def token_policy() -> TokenPolicy:
    return TokenPolicy(
        issuer="test",
        audience="test",
    )


@pytest.fixture(scope="session")
def claims_factory(token_policy: TokenPolicy) -> ClaimsFactory:
    return ClaimsFactory(token_policy)


@pytest.fixture
def refresh_claims(claims_factory: ClaimsFactory, sub: str) -> Claims:
    return claims_factory.refresh_claims(sub)


@pytest.fixture
def access_claims(claims_factory: ClaimsFactory, sub: str) -> Claims:
    return claims_factory.access_claims(sub)

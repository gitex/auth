from datetime import timedelta
from uuid import uuid4

import pytest

from src.claims import Claims, ClaimsFactory
from src.codecs.jose import JoseJwtCodec
from src.constants import DEFAULT_ALGORITHM
from src.dto import JwtSpec


@pytest.fixture(scope="session")
def ts() -> int:
    return 1759420090


@pytest.fixture
def sub() -> str:
    return uuid4().hex


@pytest.fixture(scope="session")
def jwt_spec() -> JwtSpec:
    return JwtSpec(
        alg="HS256",
        iss="test",
        aud="test",
        access_ttl=timedelta(minutes=5),
        refresh_ttl=timedelta(hours=1),
    )


@pytest.fixture
def jwt_codec() -> JoseJwtCodec:
    return JoseJwtCodec("test-secret", DEFAULT_ALGORITHM)


@pytest.fixture(scope="session")
def claims_factory(jwt_spec: JwtSpec) -> ClaimsFactory:
    return ClaimsFactory(jwt_spec)


@pytest.fixture
def refresh_claims(claims_factory: ClaimsFactory, sub: str) -> Claims:
    return claims_factory.refresh_claims(sub)


@pytest.fixture
def access_claims(claims_factory: ClaimsFactory, sub: str) -> Claims:
    return claims_factory.access_claims(sub)

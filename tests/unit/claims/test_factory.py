import time_machine

from src.claims import ClaimsFactory
from src.dto import JwtSpec


def test_iat_should_be_current_time(jwt_spec: JwtSpec, ts: int, sub: str) -> None:
    with time_machine.travel(ts, tick=False):
        factory = ClaimsFactory(jwt_spec)

        at = factory.access_claims(sub)
        rt = factory.refresh_claims(sub)

    assert at.iss == jwt_spec.iss
    assert at.aud == jwt_spec.aud
    assert at.sub == sub
    assert at.iat == ts
    assert at.nbf == ts
    assert at.exp == ts + jwt_spec.access_ttl.total_seconds()

    assert rt.iss == jwt_spec.iss
    assert rt.aud == jwt_spec.aud
    assert rt.sub == sub
    assert rt.iat == ts
    assert rt.nbf == ts
    assert rt.exp == ts + jwt_spec.refresh_ttl.total_seconds()


def test_jti_should_be_unique(claims_factory: ClaimsFactory, sub: str) -> None:
    at = claims_factory.access_claims(sub)
    rt = claims_factory.refresh_claims(sub)

    assert at.jti is not None
    assert rt.jti is not None
    assert at.jti != rt.jti


def test_nbf_should_be_iat_when_not_declared(
    claims_factory: ClaimsFactory, sub: str
) -> None:
    at = claims_factory.access_claims(sub)
    rt = claims_factory.refresh_claims(sub)

    assert at.iat is not None
    assert at.iat == at.nbf

    assert rt.iat is not None
    assert rt.iat == rt.nbf


def test_nbf_should_affect_exp(
    jwt_spec: JwtSpec, claims_factory: ClaimsFactory, ts: int, sub: str
) -> None:
    nbf = ts + 1000

    at = claims_factory.access_claims(sub, nbf=nbf)
    assert at.nbf == nbf
    assert at.exp == nbf + jwt_spec.access_ttl.total_seconds()

    rt = claims_factory.refresh_claims(sub, nbf=nbf)
    assert rt.nbf == nbf
    assert rt.exp == nbf + jwt_spec.refresh_ttl.total_seconds()

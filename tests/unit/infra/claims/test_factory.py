import time_machine

from src.domain.factories.claims import ClaimsFactory

from src.bootstrap.wiring import AuthContainer


def test_iat_should_be_current_time(
    ts: int,
    sub: str,
    claims_factory: ClaimsFactory,
    container: AuthContainer,
) -> None:
    with time_machine.travel(ts, tick=False):
        at = claims_factory.access_claims(sub)
        rt = claims_factory.refresh_claims(sub)

    spec = container.token_specification()

    assert at.iss == spec.realm.issuer
    assert at.aud == spec.realm.audience
    assert at.sub == sub
    assert at.iat == ts
    assert at.nbf == ts
    assert at.exp == ts + spec.lifetime.access_ttl_seconds

    assert rt.iss == spec.realm.issuer
    assert rt.aud == spec.realm.audience
    assert rt.sub == sub
    assert rt.iat == ts
    assert rt.nbf == ts
    assert rt.exp == ts + spec.lifetime.refresh_ttl_seconds


def test_jti_should_be_unique(claims_factory: ClaimsFactory, sub: str) -> None:
    at = claims_factory.access_claims(sub)
    rt = claims_factory.refresh_claims(sub)

    assert at.jti is not None
    assert rt.jti is not None
    assert at.jti != rt.jti


def test_nbf_should_be_iat_when_not_declared(
    claims_factory: ClaimsFactory,
    sub: str,
) -> None:
    at = claims_factory.access_claims(sub)
    rt = claims_factory.refresh_claims(sub)

    assert at.iat is not None
    assert at.iat == at.nbf

    assert rt.iat is not None
    assert rt.iat == rt.nbf


def test_nbf_should_affect_exp(ts: int, sub: str, container: AuthContainer) -> None:
    nbf = ts + 1000

    claims_factory = container.claims_factory()
    spec = container.token_specification()

    at = claims_factory.access_claims(sub, nbf=nbf)
    assert at.nbf == nbf
    assert at.exp == nbf + spec.lifetime.access_ttl_seconds

    rt = claims_factory.refresh_claims(sub, nbf=nbf)
    assert rt.nbf == nbf
    assert rt.exp == nbf + spec.lifetime.refresh_ttl_seconds

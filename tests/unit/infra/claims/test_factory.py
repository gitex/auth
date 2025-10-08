import time_machine

from src.infra.claims import ClaimsFactory
from src.infra.claims.policies import TokenPolicy
from src.infra.claims.value_objects import Timestamp


def test_iat_should_be_current_time(
    token_policy: TokenPolicy, ts: Timestamp, sub: str
) -> None:
    with time_machine.travel(ts.value, tick=False):
        factory = ClaimsFactory(token_policy)

        at = factory.access_claims(sub)
        rt = factory.refresh_claims(sub)

    assert at.iss == token_policy.issuer
    assert at.aud == token_policy.audience
    assert at.sub == sub
    assert at.iat == ts
    assert at.nbf == ts
    assert at.exp == ts.add_timedelta(token_policy.access_ttl)

    assert rt.iss == token_policy.issuer
    assert rt.aud == token_policy.audience
    assert rt.sub == sub
    assert rt.iat == ts
    assert rt.nbf == ts
    assert rt.exp == ts.add_timedelta(token_policy.refresh_ttl)


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


def test_nbf_should_affect_exp(
    token_policy: TokenPolicy, claims_factory: ClaimsFactory, ts: Timestamp, sub: str
) -> None:
    nbf = ts.add_seconds(1000)

    at = claims_factory.access_claims(sub, nbf=nbf)
    assert at.nbf == nbf
    assert at.exp == nbf.add_timedelta(token_policy.access_ttl)

    rt = claims_factory.refresh_claims(sub, nbf=nbf)
    assert rt.nbf == nbf
    assert rt.exp == nbf.add_timedelta(token_policy.refresh_ttl)

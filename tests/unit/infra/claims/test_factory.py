import time_machine

from src.infra.claims import ClaimsFactory
from src.infra.claims.policies import TokenPolicy
from src.infra.claims.value_objects import Timestamp


def test_iat_should_be_current_time(token_policy, ts: int, sub: str) -> None:
    with time_machine.travel(ts, tick=False):
        factory = ClaimsFactory(token_policy)

        at = factory.access_claims(sub)
        rt = factory.refresh_claims(sub)

    assert at.iss == token_policy.iss
    assert at.aud == token_policy.aud
    assert at.sub == sub
    assert at.iat == ts
    assert at.nbf == ts
    assert at.exp == ts + token_policy.access_ttl.total_seconds()

    assert rt.iss == token_policy.iss
    assert rt.aud == token_policy.aud
    assert rt.sub == sub
    assert rt.iat == ts
    assert rt.nbf == ts
    assert rt.exp == ts + token_policy.refresh_ttl.total_seconds()


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
    token_policy: TokenPolicy, claims_factory: ClaimsFactory, ts: int, sub: str
) -> None:
    nbf = ts + 1000

    at = claims_factory.access_claims(sub, nbf=Timestamp(nbf))
    assert at.nbf == nbf
    assert at.exp == nbf + token_policy.access_ttl.total_seconds()

    rt = claims_factory.refresh_claims(sub, nbf=Timestamp(nbf))
    assert rt.nbf == nbf
    assert rt.exp == nbf + token_policy.refresh_ttl.total_seconds()

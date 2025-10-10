import time
from dataclasses import dataclass
from datetime import timedelta
from uuid import uuid4

from src.domain.value_objects import Claims
from src.domain.value_objects.token import TokenSpecification


class ClaimFactory:
    def iat(self) -> int:
        """Issued at (unix time)"""
        return int(time.time())

    def jti(self) -> str:
        """JWT Identifier"""
        return uuid4().hex

    def exp(self, base: int, ttl: timedelta) -> int:
        """Expiration time (unix time)"""
        return base + int(ttl.total_seconds())


@dataclass(slots=True)
class ClaimsFactory:
    """Фабрика для создания Claims."""

    spec: TokenSpecification

    def _base_claims(self, sub: str, ttl: timedelta, nbf: int | None = None) -> Claims:
        claim_factory = ClaimFactory()

        claims = {
            'sub': sub,
            'jti': claim_factory.jti(),
            'iat': claim_factory.iat(),
        }

        if iss := self.spec.realm.issuer:
            claims['iss'] = iss

        if aud := self.spec.realm.audience:
            claims['aud'] = aud

        if active_at := nbf or claims['iat']:
            claims['nbf'] = active_at
            claims['exp'] = claim_factory.exp(base=active_at, ttl=ttl)
        return Claims(**claims)

    def access_claims(self, sub: str, nbf: int | None = None) -> Claims:
        return self._base_claims(sub, nbf=nbf, ttl=self.spec.lifetime.access_ttl)

    def refresh_claims(self, sub: str, nbf: int | None = None) -> Claims:
        return self._base_claims(sub, nbf=nbf, ttl=self.spec.lifetime.refresh_ttl)

from dataclasses import dataclass
from datetime import timedelta
from uuid import uuid4

from .entities import Claims
from .policies import TokenPolicy
from .value_objects import Timestamp


class ClaimFactory:
    """Фабрика базовых типов Claims."""

    def jti(self) -> str:
        """(JWT ID): уникальный идентификатор токена."""
        return uuid4().hex

    def exp(self, base: Timestamp, ttl: timedelta) -> Timestamp:
        """(Expiration Time): Unix время истечения токена."""
        return base.add_seconds(int(ttl.total_seconds()))

    def iat(self) -> Timestamp:
        """(Issued At): Unix время создания токена."""
        return Timestamp.now()


@dataclass
class ClaimsFactory:
    """Фабрика для создания Claims.

    Attributes:
        jwt_spec: Общая спецификация для Jwt
    """

    policy: TokenPolicy
    claim_factory: ClaimFactory = ClaimFactory()

    def _base_claims(
        self, sub: str, ttl: timedelta, nbf: Timestamp | None = None
    ) -> Claims:
        claims = Claims(sub=sub, jti=self.claim_factory.jti())

        iat = self.claim_factory.iat()
        claims.iat = iat

        if iss := self.policy.issuer:
            claims.iss = iss

        if aud := self.policy.audience:
            claims.aud = aud

        if nbf:
            claims.nbf = nbf
            claims.exp = self.claim_factory.exp(base=nbf, ttl=ttl)
        elif iat:
            claims.nbf = iat
            claims.exp = self.claim_factory.exp(base=iat, ttl=ttl)

        return claims

    def access_claims(self, sub: str, nbf: Timestamp | None = None) -> Claims:
        """Claims для создания access token."""

        return self._base_claims(sub, nbf=nbf, ttl=self.policy.access_ttl)

    def refresh_claims(self, sub: str, nbf: Timestamp | None = None) -> Claims:
        """Claims для создания refresh token."""

        return self._base_claims(sub, nbf=nbf, ttl=self.policy.refresh_ttl)

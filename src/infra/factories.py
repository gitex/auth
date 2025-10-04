from datetime import timedelta
from typing import final
from uuid import uuid4

from src.dto import JwtSpec

from .entities import Claims, PrivateClaims
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


@final
class ClaimsFactory:
    """Фабрика для создания Claims.

    Attributes:
        jwt_spec: Общая спецификация для Jwt
    """

    def __init__(self, jwt_spec: JwtSpec) -> None:
        self.jwt_spec = jwt_spec
        self._factory = ClaimFactory()

    def _base_claims(
        self, sub: str, ttl: timedelta, nbf: Timestamp | None = None
    ) -> Claims:
        claims = Claims(sub=sub, jti=self._factory.jti())

        iat = self._factory.iat()
        claims.iat = iat

        if iss := self.jwt_spec.iss:
            claims.iss = iss

        if aud := self.jwt_spec.aud:
            claims.aud = aud

        if nbf:
            claims.nbf = nbf
            claims.exp = self._factory.exp(base=nbf, ttl=ttl)
        elif iat:
            claims.nbf = iat
            claims.exp = self._factory.exp(base=iat, ttl=ttl)

        return claims

    def access_claims(
        self,
        sub: str,
        nbf: Timestamp | None = None,
        custom_claims: PrivateClaims | None = None,
    ) -> Claims:
        """Claims для создания access token."""

        claims = self._base_claims(sub, nbf=nbf, ttl=self.jwt_spec.access_ttl)

        if custom_claims:
            claims = claims.update(custom_claims)

        return claims

    def refresh_claims(self, sub: str, nbf: int | None = None) -> Claims:
        """Claims для создания refresh token."""

        return self._base_claims(sub, nbf=nbf, ttl=self.jwt_spec.refresh_ttl)

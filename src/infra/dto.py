from __future__ import annotations

import typing as tp
from dataclasses import asdict, dataclass

from src.domain.value_objects.claims import Claims


@dataclass(frozen=True, slots=True)
class ClaimsDto:
    sub: str | None = None
    aud: str | None = None
    iss: str | None = None
    iat: int | None = None
    exp: int | None = None
    nbf: int | None = None
    jti: str | None = None
    email: str | None = None
    scope: str | None = None

    @classmethod
    def from_claims(cls, claims: Claims) -> ClaimsDto:
        aud = ' '.join([c.lower() for c in claims.aud]) if claims.aud else None

        return cls(
            sub=claims.sub,
            aud=aud,
            iss=claims.iss,
            iat=claims.iat,
            exp=claims.exp,
            nbf=claims.nbf,
            jti=claims.jti,
            email=claims.email,
            scope=claims.scope,
        )

    def as_claims(self) -> Claims:
        aud = self.aud.split(' ') if self.aud else None

        return Claims(
            sub=self.sub,
            iss=self.iss,
            aud=aud,
            iat=self.iat,
            exp=self.exp,
            nbf=self.nbf,
            jti=self.jti,
            email=self.email,
            scope=self.scope,
        )

    def as_dict(self, *, exclude_none: bool = False) -> dict[str, tp.Any]:
        """Form dict and exclude empty claims."""
        output = {}

        for key, value in asdict(self).items():
            if exclude_none and value is None:
                continue

            output[key] = value

        return output

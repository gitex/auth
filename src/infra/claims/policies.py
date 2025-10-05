from dataclasses import dataclass, field
from datetime import timedelta
from enum import Enum
from typing import Literal

from .entities import Claims


class TokenError(str, Enum):
    REQUIRED_SUB = "required_sub"
    REQUIRED_JTI = "required_jti"
    REQUIRED_EXP = "required_exp"
    WRONG_ISSUER = "wrong_issuer"
    WRONG_AUDIENCE = "wrong_audience"


@dataclass
class TokenPolicy:
    """TTL, состав claims, audience/issuer, clock-skew."""

    issuer: str
    audience: str

    # Алгоритмы подписи
    algorithm: Literal["HS256", "RS256"] = field(default="HS256")

    # TTL, skew (отклонение)
    access_ttl: timedelta = timedelta(minutes=15)
    refresh_ttl: timedelta = timedelta(days=7)
    skew: timedelta = timedelta(seconds=30)

    # Требования к claims
    require_sub: bool = True
    require_jti: bool = True
    require_exp: bool = True

    def validate(self, claims: Claims) -> tuple[bool, list[TokenError]]:
        errors: list[TokenError] = []

        if self.require_sub and not claims.sub:
            errors.append(TokenError.REQUIRED_SUB)
        if self.require_jti and not claims.jti:
            errors.append(TokenError.REQUIRED_JTI)
        if self.require_exp and not claims.exp:
            errors.append(TokenError.REQUIRED_EXP)

        if claims.aud != self.audience:
            errors.append(TokenError.WRONG_AUDIENCE)
        if claims.iss != self.issuer:
            errors.append(TokenError.WRONG_ISSUER)

        if errors:
            return False, errors
        return True, errors

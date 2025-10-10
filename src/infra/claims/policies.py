from dataclasses import dataclass, field
from datetime import timedelta
from typing import Literal


@dataclass
class TokenPolicy:
    """"""

    """TTL, состав claims, audience/issuer, clock-skew."""

    issuer: str
    audience: str

    # Алгоритмы подписи
    algorithm: Literal['HS256', 'RS256'] = field(default='HS256')

    access_ttl: timedelta = timedelta(minutes=15)
    refresh_ttl: timedelta = timedelta(days=7)
    skew: timedelta = timedelta(seconds=30)

    # Требования к claims
    require_sub: bool = True
    require_jti: bool = True
    require_exp: bool = True

    def validate(self) -> tuple[bool, list[str]]:
        return True, []

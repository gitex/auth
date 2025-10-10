from dataclasses import dataclass
from datetime import timedelta


@dataclass(frozen=True, slots=True)
class TokenRealm:
    issuer: str
    audience: list[str]


@dataclass(frozen=True, slots=True)
class TokenLifetime:
    access_ttl: timedelta
    refresh_ttl: timedelta
    clock_skew: timedelta

    @property
    def access_ttl_seconds(self) -> int:
        return int(self.access_ttl.total_seconds())

    @property
    def refresh_ttl_seconds(self) -> int:
        return int(self.refresh_ttl.total_seconds())


@dataclass(frozen=True, slots=True)
class TokenSpecification:
    realm: TokenRealm
    lifetime: TokenLifetime

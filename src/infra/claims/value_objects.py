import time
from dataclasses import dataclass
from datetime import timedelta
from typing import Self
from uuid import UUID, uuid4


def value_should_be_positive(value: int) -> None:
    """Validate if value is positive

    :raise ValueError
    """
    if value < 0:
        raise ValueError("Value must be positive")  # TODO: Change exception


@dataclass(frozen=True)
class TTL:
    seconds: int

    def __post_init__(self) -> None:
        value_should_be_positive(self.seconds)

    @classmethod
    def from_timedelta(cls, delta: timedelta) -> "TTL":
        return cls(int(delta.total_seconds()))

    def __int__(self) -> int:
        return self.seconds


@dataclass(frozen=True)
class Timestamp:
    """Unix timestamp."""

    value: int

    def __post_init__(self) -> None:
        value_should_be_positive(self.value)

    @classmethod
    def now(cls) -> Self:
        return cls(int(time.time()))

    def add_seconds(self, seconds: int) -> "Timestamp":
        return Timestamp(self.value + seconds)

    def add_ttl(self, ttl: TTL) -> "Timestamp":
        return self.add_seconds(ttl.seconds)

    def __int__(self) -> int:
        return int(self.value)


@dataclass(frozen=True)
class Token: ...


@dataclass(frozen=True)
class AccessToken:
    value: str


@dataclass(frozen=True)
class RefreshToken:
    value: str


@dataclass(frozen=True)
class Jti:  # TODO убрать, не domain
    value: UUID

    @classmethod
    def new(cls) -> "Jti":
        return cls(uuid4())

    def __str__(self) -> str:
        return str(self.value)

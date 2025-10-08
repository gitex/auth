from collections.abc import Iterator
from dataclasses import dataclass
from datetime import timedelta

from src.domain.exceptions import ShouldBePositiveError


def value_should_be_positive(value: int) -> None:
    """Validate if value is positive

    :raise ValueError
    """
    if value < 0:
        raise ShouldBePositiveError({'value': value})


@dataclass(frozen=True, slots=True)
class TTL:
    seconds: int

    def __post_init__(self) -> None:
        value_should_be_positive(self.seconds)

    @classmethod
    def from_timedelta(cls, delta: timedelta) -> 'TTL':
        return cls(int(delta.total_seconds()))

    def __int__(self) -> int:
        return self.seconds


@dataclass(frozen=True, slots=True)
class RefreshSessionId:
    value: str


@dataclass(frozen=True, slots=True)
class RefreshFamilyId:
    """Цепочка ротаций."""

    value: str


@dataclass(frozen=True, slots=True)
class AccessToken:
    value: str

    def __str__(self) -> str:
        return str(self.value)


@dataclass(frozen=True, slots=True)
class RefreshToken:
    value: str

    def __str__(self) -> str:
        return str(self.value)


@dataclass(frozen=True, slots=True)
class Email:
    value: str


@dataclass(frozen=True, slots=True)
class Password:
    value: str

    def __len__(self) -> int:
        return len(self.value)

    def __iter__(self) -> Iterator[str]:
        yield from iter(self.value)


@dataclass(frozen=True, slots=True)
class PasswordHash:
    value: str


@dataclass(frozen=True, slots=True)
class Scope:
    name: str

    def __str__(self) -> str:
        return self.name.strip().lower()


@dataclass(frozen=True, slots=True)
class Role:
    name: str

    def __str__(self) -> str:
        return self.name.strip().lower()

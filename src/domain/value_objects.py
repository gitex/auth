from collections.abc import Iterator
from dataclasses import dataclass
from datetime import timedelta

from .exceptions import ValidationError


def value_should_be_positive(value: int) -> None:
    """Validate if value is positive

    :raise ValueError
    """
    if value < 0:
        raise ValidationError("Value must be positive")


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
class RefreshSessionId:
    value: str


@dataclass(frozen=True)
class RefreshFamilyId:
    """Цепочка ротаций."""

    value: str


@dataclass(frozen=True)
class AccessToken:
    value: str

    def __str__(self) -> str:
        return str(self.value)


@dataclass(frozen=True)
class RefreshToken:
    value: str

    def __str__(self) -> str:
        return str(self.value)


@dataclass(frozen=True)
class Email:
    value: str


@dataclass(frozen=True)
class Password:
    value: str

    def __len__(self) -> int:
        return len(self.value)

    def __iter__(self) -> Iterator[str]:
        yield from iter(self.value)


@dataclass(frozen=True)
class PasswordHash:
    value: str


@dataclass(frozen=True)
class Scope:
    name: str

    def __post_init__(self) -> None:
        assert self.name and self.name.islower() and " " not in self.name


@dataclass(frozen=True)
class Role:
    name: str

    def __post_init__(self) -> None:
        assert self.name and self.name.islower() and " " not in self.name

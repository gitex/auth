from dataclasses import dataclass
from datetime import UTC, datetime, timedelta


@dataclass(frozen=True, slots=True)
class ClockSkew:
    seconds: int

    def as_duration(self) -> 'Duration':
        return Duration.seconds(self.seconds)


@dataclass(frozen=True, slots=True)
class Duration:
    delta: timedelta

    @classmethod
    def seconds(cls, seconds: int) -> 'Duration':
        return cls(timedelta(seconds=seconds))

    @classmethod
    def minutes(cls, minutes: int) -> 'Duration':
        return cls(timedelta(minutes=minutes))


@dataclass(frozen=True, slots=True)
class Instant:
    dt: datetime

    @classmethod
    def now(cls) -> 'Instant':
        return cls(datetime.now(UTC))

    @classmethod
    def from_epoch(cls, sec: int) -> 'Instant':
        return cls(datetime.fromtimestamp(sec, UTC))

    def as_epoch(self) -> int:
        return int(self.dt.timestamp())

    def __lt__(self, other: 'Instant') -> bool:
        return self.dt < other.dt

    def __add__(self, d: Duration) -> 'Instant':
        return Instant(self.dt + d.delta)


@dataclass(frozen=True, slots=True)
class Expiration:
    at: Instant

    @classmethod
    def from_now(cls, duration: Duration, now: Instant | None = None) -> 'Expiration':
        now = now or Instant.now()
        return cls(Instant(now.dt + duration.delta))

    def is_expired(self, skew: ClockSkew) -> bool:
        return (self.at + skew.as_duration()) < Instant.now()

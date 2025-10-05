from collections.abc import Callable
from dataclasses import dataclass
from datetime import timedelta
from enum import Enum, auto

from domain.value_objects import Password


class PasswordError(Enum):
    TOO_SHORT = auto()
    TOO_LONG = auto()
    REQUIRE_LOWER = auto()
    REQUIRE_UPPER = auto()
    REQUIRE_DIGIT = auto()
    REQUIRE_SYMBOL = auto()


SYMBOLS = set(r"!@#$%^&*()-_=+[]{};:'\",.<>/?\|`~")


@dataclass(frozen=True)
class PasswordPolicy:
    min_length: int = 10
    max_length: int = 100

    require_lower: bool = True
    require_upper: bool = True
    require_digit: bool = True
    require_symbols: bool = True

    max_repeats: int = 3  # "aaaa"
    max_sequential: int = 4  # "abcd" | "1234"

    blacklist: frozenset[str] = frozenset({"password", "qwerty", "12345"})

    expires_in: timedelta = timedelta(days=365)

    def validate(self, password: Password) -> list[PasswordError]:
        errors: list[PasswordError] = []

        n = len(password)

        if n < self.min_length:
            errors.append(PasswordError.TOO_SHORT)
        if n > self.max_length:
            errors.append(PasswordError.TOO_LONG)

        def password_has(f: Callable[[str], bool]) -> bool:
            return any(f(c) for c in password)

        if self.require_lower and not password_has(str.islower):
            errors.append(PasswordError.REQUIRE_LOWER)
        if self.require_upper and not password_has(str.isupper):
            errors.append(PasswordError.REQUIRE_UPPER)
        if self.require_digit and not password_has(str.isdigit):
            errors.append(PasswordError.REQUIRE_DIGIT)
        if self.require_symbols and not any(c in SYMBOLS for c in password):
            errors.append(PasswordError.REQUIRE_SYMBOL)

        return errors

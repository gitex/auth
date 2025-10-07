from collections.abc import Callable
from dataclasses import dataclass
from datetime import timedelta
from enum import Enum

from src.domain.value_objects import Password


class PasswordError(Enum):
    TOO_SHORT = "too_short"
    TOO_LONG = "too_long"
    REQUIRE_LOWER = "require_lower"
    REQUIRE_UPPER = "require_upper"
    REQUIRE_DIGIT = "require_digit"
    REQUIRE_SYMBOL = "require_symbol"


SYMBOLS = set(r"!@#$%^&*()-_=+[]{};:'\",.<>/?\|`~")


@dataclass(frozen=True)
class PasswordPolicy:
    min_length: int = 10
    max_length: int = 100

    require_lower: bool = True
    require_upper: bool = True
    require_digit: bool = True
    require_symbol: bool = True

    max_repeats: int = 3  # "aaaa"
    max_sequential: int = 4  # "abcd" | "1234"

    blacklist: frozenset[str] = frozenset({"password", "qwerty", "12345"})

    expires_in: timedelta = timedelta(days=365)

    def validate(self, password: Password) -> tuple[bool, list[str]]:
        errors: list[str] = []

        n = len(password)

        if n < self.min_length:
            errors.append(
                f"Password's length should not be less then {self.min_length}"
            )  # Строки надо куда-то выносить
        if n > self.max_length:
            errors.append(f"Password's length should not be more then {self.max_length}")

        def password_has(f: Callable[[str], bool]) -> bool:
            return any(f(c) for c in password)

        if self.require_lower and not password_has(str.islower):
            errors.append("Password should contain lowercase letter")
        if self.require_upper and not password_has(str.isupper):
            errors.append("Password should contain uppercase letter")
        if self.require_digit and not password_has(str.isdigit):
            errors.append("Password should contain digit")
        if self.require_symbol and not any(c in SYMBOLS for c in password):
            errors.append("Password should contain any of special symbols")

        if errors:
            return False, errors
        return True, errors

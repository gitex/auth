from collections.abc import Iterable
from enum import Enum
from typing import Protocol, final, override

from src.domain.value_objects import Password


class PasswordError(Enum):
    TOO_SHORT = 'too_short'
    TOO_LONG = 'too_long'
    REQUIRE_LOWER = 'require_lower'
    REQUIRE_UPPER = 'require_upper'
    REQUIRE_DIGIT = 'require_digit'
    REQUIRE_SYMBOL = 'require_symbol'
    FORBIDDEN_WORD = 'forbidden_word'


SYMBOLS = set(r"!@#$%^&*()-_=+[]{};:'\",.<>/?\|`~")


class PasswordPolicy(Protocol):
    code: PasswordError

    def error_message(self) -> str: ...
    def validate(self, password: Password) -> bool: ...


@final
class PasswordPolicySuite:
    def __init__(self, policies: Iterable[PasswordPolicy]) -> None:
        self._policies = policies

    def validate(self, password: Password) -> tuple[bool, list[str]]:
        errors: list[str] = []

        for policy in self._policies:
            is_valid = policy.validate(password)

            if not is_valid:
                errors.append(policy.error_message())

        if errors:
            return False, errors
        return True, errors


@final
class PasswordContainUpperacacePolicy(PasswordPolicy):
    code: PasswordError = PasswordError.REQUIRE_UPPER

    @override
    def validate(self, password: Password) -> bool:
        return password.any_of_characters(str.isupper)

    @override
    def error_message(self) -> str:
        return 'Password should contain uppercase letter'


@final
class PasswordContainLowercasePolicy(PasswordPolicy):
    code: PasswordError = PasswordError.REQUIRE_LOWER

    @override
    def validate(self, password: Password) -> bool:
        return password.any_of_characters(str.islower)

    @override
    def error_message(self) -> str:
        return 'Password should contain lowercase letter'


@final
class PasswordMinLengthPolicy(PasswordPolicy):
    code: PasswordError = PasswordError.TOO_SHORT

    def __init__(self, min_length: int) -> None:
        self._min_length = min_length

    @override
    def validate(self, password: Password) -> bool:
        return len(password) >= self._min_length

    @override
    def error_message(self) -> str:
        return f'Password should be at least {self._min_length} symbols long.'


@final
class PasswordMaxLengthPolicy(PasswordPolicy):
    code: PasswordError = PasswordError.TOO_LONG

    def __init__(self, max_length: int) -> None:
        self._max_length = max_length

    @override
    def validate(self, password: Password) -> bool:
        return len(password) <= self._max_length

    @override
    def error_message(self) -> str:
        return f'Password should not be more than {self._max_length} symbols'


@final
class PasswordNotInBlacklistPolicy(PasswordPolicy):
    code: PasswordError = PasswordError.FORBIDDEN_WORD

    def __init__(self, blacklist: set[str]) -> None:
        self._blacklist = blacklist

    @override
    def validate(self, password: Password) -> bool:
        return password.value in self._blacklist

    @override
    def error_message(self) -> str:
        return 'Password is too simple'

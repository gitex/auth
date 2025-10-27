import pytest

from src.domain.policies.password import (
    PasswordMaxLengthPolicy,
    PasswordMinLengthPolicy,
)
from src.domain.value_objects import Password


@pytest.mark.parametrize(
    'value,expected',
    [
        ('abcd', False),
        ('abcde', True),
    ],
)
def test_min_length_policy_boundary(value: str, expected: bool) -> None:
    policy = PasswordMinLengthPolicy(5)

    assert policy.validate(Password(value=value)) is expected


@pytest.mark.parametrize(
    'value,expected',
    [
        ('abcdefghijk', False),
        ('abcdefghij', True),
    ],
)
def test_max_length_policy_boundary(value: str, expected: bool) -> None:
    policy = PasswordMaxLengthPolicy(10)

    assert policy.validate(Password(value=value)) is expected

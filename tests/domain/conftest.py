"""Fixtures for domain tests.

Domain tests are pure unit tests that don't require database,
HTTP client, or dependency injection.
"""

import pytest

from src.domain.value_objects import Email, Password, PasswordHash


@pytest.fixture
def sample_email() -> Email:
    """Sample Email value object for tests."""
    return Email('test@example.com')


@pytest.fixture
def sample_password() -> Password:
    """Sample Password value object for tests."""
    return Password('Test@Pass123')


@pytest.fixture
def sample_password_hash() -> PasswordHash:
    """Sample PasswordHash value object for tests."""
    return PasswordHash('$2b$12$abcdefghijklmnopqrstuvwxyz012345678901234567890')

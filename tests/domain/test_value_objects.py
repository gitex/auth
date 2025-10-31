"""Tests for domain value objects.

These tests verify immutability, validation, and behavior of value objects.
"""

import pytest

from src.domain.value_objects import Email, Password, PasswordHash, Role


class TestEmail:
    """Tests for Email value object."""

    def test_email_is_frozen(self) -> None:
        """Test that Email is immutable."""
        email = Email('test@example.com')

        with pytest.raises(AttributeError):
            email.value = 'other@example.com'  # type: ignore[misc]

    def test_email_equality(self) -> None:
        """Test that emails with same value are equal."""
        email1 = Email('test@example.com')
        email2 = Email('test@example.com')

        assert email1 == email2

    def test_email_stores_value(self) -> None:
        """Test that email stores its value correctly."""
        email = Email('test@example.com')

        assert email.value == 'test@example.com'


class TestPassword:
    """Tests for Password value object."""

    def test_password_is_frozen(self) -> None:
        """Test that Password is immutable."""
        password = Password('secret123')

        with pytest.raises(AttributeError):
            password.value = 'other'  # type: ignore[misc]

    def test_password_length(self) -> None:
        """Test password length calculation."""
        password = Password('secret123')

        assert len(password) == 9

    def test_password_iteration(self) -> None:
        """Test that password can be iterated."""
        password = Password('abc')

        chars = list(password)

        assert chars == ['a', 'b', 'c']

    def test_password_any_of_characters_returns_true(self) -> None:
        """Test any_of_characters returns True when condition matches."""
        password = Password('abc123')

        assert password.any_of_characters(str.isdigit) is True

    def test_password_any_of_characters_returns_false(self) -> None:
        """Test any_of_characters returns False when condition doesn't match."""
        password = Password('abc')

        assert password.any_of_characters(str.isdigit) is False

    def test_password_equality(self) -> None:
        """Test that passwords with same value are equal."""
        password1 = Password('secret')
        password2 = Password('secret')

        assert password1 == password2


class TestPasswordHash:
    """Tests for PasswordHash value object."""

    def test_password_hash_is_frozen(self) -> None:
        """Test that PasswordHash is immutable."""
        password_hash = PasswordHash('$2b$12$abcdef')

        with pytest.raises(AttributeError):
            password_hash.value = 'other'  # type: ignore[misc]

    def test_password_hash_equality(self) -> None:
        """Test that password hashes with same value are equal."""
        hash1 = PasswordHash('$2b$12$abcdef')
        hash2 = PasswordHash('$2b$12$abcdef')

        assert hash1 == hash2

    def test_password_hash_stores_value(self) -> None:
        """Test that password hash stores its value correctly."""
        password_hash = PasswordHash('$2b$12$abcdef')

        assert password_hash.value == '$2b$12$abcdef'


class TestRole:
    """Tests for Role value object."""

    def test_role_is_frozen(self) -> None:
        """Test that Role is immutable."""
        role = Role('admin')

        with pytest.raises(AttributeError):
            role.name = 'user'  # type: ignore[misc]

    def test_role_to_string(self) -> None:
        """Test role string representation."""
        role = Role('Admin')

        assert str(role) == 'admin'

    def test_role_normalizes_to_lowercase(self) -> None:
        """Test that role name is normalized to lowercase."""
        role = Role(' ADMIN ')

        assert str(role) == 'admin'

    def test_role_equality(self) -> None:
        """Test that roles with same name are equal."""
        role1 = Role('admin')
        role2 = Role('admin')

        assert role1 == role2

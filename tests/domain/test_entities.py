"""Tests for domain entities.

These are pure unit tests that don't require database, mocks, or dependency injection.
They test business logic and invariants of domain entities.
"""

from uuid import uuid4

import pytest

from src.domain.entities import Account
from src.domain.events import (
    AccountActivated,
    AccountDeactivated,
    AccountPasswordChanged,
)
from src.domain.value_objects import Email, PasswordHash, Role


class TestAccountAggregateRoot:
    """Tests for Account as Aggregate Root."""

    def test_change_password_emits_event(self) -> None:
        """Test that changing password emits AccountPasswordChanged event."""
        account = Account(
            identifier=uuid4(),
            email=Email('test@example.com'),
            password_hash=PasswordHash('old_hash'),
            is_active=True,
        )

        new_hash = PasswordHash('new_hash')
        event = account.change_password(new_hash)

        assert isinstance(event, AccountPasswordChanged)
        assert event.email == account.email
        assert account.password_hash == new_hash

    def test_change_password_updates_hash(self) -> None:
        """Test that changing password actually updates the hash."""
        account = Account(
            identifier=uuid4(),
            email=Email('test@example.com'),
            password_hash=PasswordHash('old_hash'),
            is_active=True,
        )

        new_hash = PasswordHash('new_hash')
        account.change_password(new_hash)

        assert account.password_hash.value == 'new_hash'

    def test_change_password_raises_for_inactive_account(self) -> None:
        """Test that changing password fails for inactive account."""
        account = Account(
            identifier=uuid4(),
            email=Email('test@example.com'),
            password_hash=PasswordHash('hash'),
            is_active=False,
        )

        with pytest.raises(ValueError, match='Cannot change password for inactive'):
            account.change_password(PasswordHash('new_hash'))

    def test_activate_changes_status(self) -> None:
        """Test that activate changes account status."""
        account = Account(
            identifier=uuid4(),
            email=Email('test@example.com'),
            password_hash=PasswordHash('hash'),
            is_active=False,
        )

        event = account.activate()

        assert isinstance(event, AccountActivated)
        assert event.email == account.email
        assert account.is_active is True

    def test_activate_raises_if_already_active(self) -> None:
        """Test that activating an active account raises error."""
        account = Account(
            identifier=uuid4(),
            email=Email('test@example.com'),
            password_hash=PasswordHash('hash'),
            is_active=True,
        )

        with pytest.raises(ValueError, match='already active'):
            account.activate()

    def test_deactivate_changes_status(self) -> None:
        """Test that deactivate changes account status."""
        account = Account(
            identifier=uuid4(),
            email=Email('test@example.com'),
            password_hash=PasswordHash('hash'),
            is_active=True,
        )

        event = account.deactivate()

        assert isinstance(event, AccountDeactivated)
        assert event.email == account.email
        assert account.is_active is False

    def test_deactivate_raises_if_already_inactive(self) -> None:
        """Test that deactivating an inactive account raises error."""
        account = Account(
            identifier=uuid4(),
            email=Email('test@example.com'),
            password_hash=PasswordHash('hash'),
            is_active=False,
        )

        with pytest.raises(ValueError, match='already inactive'):
            account.deactivate()

    def test_add_role_success(self) -> None:
        """Test adding a new role to account."""
        account = Account(
            identifier=uuid4(),
            email=Email('test@example.com'),
            password_hash=PasswordHash('hash'),
            is_active=True,
            roles=[],
        )

        role = Role('admin')
        account.add_role(role)

        assert role in account.roles
        assert len(account.roles) == 1

    def test_add_role_raises_if_exists(self) -> None:
        """Test that adding duplicate role raises error."""
        role = Role('admin')
        account = Account(
            identifier=uuid4(),
            email=Email('test@example.com'),
            password_hash=PasswordHash('hash'),
            is_active=True,
            roles=[role],
        )

        with pytest.raises(ValueError, match='already exists'):
            account.add_role(role)

    def test_remove_role_success(self) -> None:
        """Test removing an existing role from account."""
        role = Role('admin')
        account = Account(
            identifier=uuid4(),
            email=Email('test@example.com'),
            password_hash=PasswordHash('hash'),
            is_active=True,
            roles=[role],
        )

        account.remove_role(role)

        assert role not in account.roles
        assert len(account.roles) == 0

    def test_remove_role_raises_if_not_exists(self) -> None:
        """Test that removing non-existent role raises error."""
        account = Account(
            identifier=uuid4(),
            email=Email('test@example.com'),
            password_hash=PasswordHash('hash'),
            is_active=True,
            roles=[],
        )

        with pytest.raises(ValueError, match='does not exist'):
            account.remove_role(Role('admin'))

    def test_has_role_returns_true_if_exists(self) -> None:
        """Test has_role returns True for existing role."""
        role = Role('admin')
        account = Account(
            identifier=uuid4(),
            email=Email('test@example.com'),
            password_hash=PasswordHash('hash'),
            is_active=True,
            roles=[role],
        )

        assert account.has_role(role) is True

    def test_has_role_returns_false_if_not_exists(self) -> None:
        """Test has_role returns False for non-existent role."""
        account = Account(
            identifier=uuid4(),
            email=Email('test@example.com'),
            password_hash=PasswordHash('hash'),
            is_active=True,
            roles=[],
        )

        assert account.has_role(Role('admin')) is False

    def test_account_invariants(self) -> None:
        """Test that account maintains its invariants."""
        email = Email('test@example.com')
        password_hash = PasswordHash('hash')
        account = Account(
            identifier=None,
            email=email,
            password_hash=password_hash,
            is_active=True,
        )

        # Email should not change
        assert account.email == email
        # Password hash should be set
        assert account.password_hash == password_hash
        # Should be active by default
        assert account.is_active is True
        # Roles should be empty list by default
        assert account.roles == []

"""Tests for RegisterService application service."""

import pytest

from src.domain.entities import Account
from src.domain.events import AccountRegistered
from src.domain.value_objects import Email, Password

from src.application.exceptions import AccountAlreadyExistsError, PasswordPolicyError
from src.application.services.register import (
    RegisterCommand,
    RegisterResult,
    RegisterService,
)

from tests.application.conftest import (
    MockEventPublisher,
    MockPasswordHasher,
    MockPasswordPolicySuite,
    MockUnitOfWork,
)


class TestRegisterService:
    """Tests for RegisterService."""

    @pytest.mark.asyncio
    async def test_successful_registration(
        self,
        mock_uow: MockUnitOfWork,
        mock_password_hasher: MockPasswordHasher,
        mock_password_policy_suite: MockPasswordPolicySuite,
        mock_event_publisher: MockEventPublisher,
        sample_email: Email,
        sample_password: Password,
    ) -> None:
        """Test successful user registration."""
        service = RegisterService(
            uow=mock_uow,
            password_hasher=mock_password_hasher,
            password_policies_suite=mock_password_policy_suite,
            event_publishers=[mock_event_publisher],
        )

        cmd = RegisterCommand(email=sample_email, password=sample_password)
        result = await service.register(cmd)

        assert isinstance(result, RegisterResult)
        assert isinstance(result.account, Account)
        assert result.account.email == sample_email
        assert result.account.is_active is True
        assert result.account.identifier is not None

        # Verify password was hashed
        mock_password_hasher.hash.assert_called_once_with(sample_password)

        # Verify account was created in repository
        mock_uow.accounts.create.assert_called_once()

        # Verify event was published
        assert len(mock_event_publisher.published_events) == 1
        event = mock_event_publisher.published_events[0]
        assert isinstance(event, AccountRegistered)
        assert event.email == sample_email

    @pytest.mark.asyncio
    async def test_registration_with_existing_email(
        self,
        mock_uow: MockUnitOfWork,
        mock_password_hasher: MockPasswordHasher,
        mock_password_policy_suite: MockPasswordPolicySuite,
        sample_email: Email,
        sample_password: Password,
        sample_account: Account,
    ) -> None:
        """Test registration fails when email already exists."""
        # Add existing account
        mock_uow.accounts.accounts[sample_email.value] = sample_account

        service = RegisterService(
            uow=mock_uow,
            password_hasher=mock_password_hasher,
            password_policies_suite=mock_password_policy_suite,
        )

        cmd = RegisterCommand(email=sample_email, password=sample_password)

        with pytest.raises(AccountAlreadyExistsError):
            await service.register(cmd)

        # Verify no account was created
        mock_uow.accounts.create.assert_not_called()

    @pytest.mark.asyncio
    async def test_registration_with_password_policy_violation(
        self,
        mock_uow: MockUnitOfWork,
        mock_password_hasher: MockPasswordHasher,
        sample_email: Email,
        sample_password: Password,
    ) -> None:
        """Test registration fails when password doesn't meet policy."""
        failing_policy = MockPasswordPolicySuite(
            should_pass=False, errors=['Password too weak']
        )

        service = RegisterService(
            uow=mock_uow,
            password_hasher=mock_password_hasher,
            password_policies_suite=failing_policy,
        )

        cmd = RegisterCommand(email=sample_email, password=sample_password)

        with pytest.raises(PasswordPolicyError):
            await service.register(cmd)

        # Verify no account was created
        mock_uow.accounts.create.assert_not_called()

        # Verify password was not hashed
        mock_password_hasher.hash.assert_not_called()

    @pytest.mark.asyncio
    async def test_registration_emits_events(
        self,
        mock_uow: MockUnitOfWork,
        mock_password_hasher: MockPasswordHasher,
        mock_password_policy_suite: MockPasswordPolicySuite,
        sample_email: Email,
        sample_password: Password,
    ) -> None:
        """Test that registration emits AccountRegistered event."""
        event_publisher1 = MockEventPublisher()
        event_publisher2 = MockEventPublisher()

        service = RegisterService(
            uow=mock_uow,
            password_hasher=mock_password_hasher,
            password_policies_suite=mock_password_policy_suite,
            event_publishers=[event_publisher1, event_publisher2],
        )

        cmd = RegisterCommand(email=sample_email, password=sample_password)
        await service.register(cmd)

        # Verify both publishers received the event
        assert len(event_publisher1.published_events) == 1
        assert len(event_publisher2.published_events) == 1

        event1 = event_publisher1.published_events[0]
        event2 = event_publisher2.published_events[0]

        assert isinstance(event1, AccountRegistered)
        assert isinstance(event2, AccountRegistered)
        assert event1.email == sample_email
        assert event2.email == sample_email

    @pytest.mark.asyncio
    async def test_registration_without_password_policy(
        self,
        mock_uow: MockUnitOfWork,
        mock_password_hasher: MockPasswordHasher,
        sample_email: Email,
        sample_password: Password,
    ) -> None:
        """Test registration works without password policy suite."""
        service = RegisterService(
            uow=mock_uow,
            password_hasher=mock_password_hasher,
            password_policies_suite=None,
        )

        cmd = RegisterCommand(email=sample_email, password=sample_password)
        result = await service.register(cmd)

        assert isinstance(result, RegisterResult)
        assert result.account.email == sample_email

    @pytest.mark.asyncio
    async def test_registration_without_event_publishers(
        self,
        mock_uow: MockUnitOfWork,
        mock_password_hasher: MockPasswordHasher,
        mock_password_policy_suite: MockPasswordPolicySuite,
        sample_email: Email,
        sample_password: Password,
    ) -> None:
        """Test registration works without event publishers."""
        service = RegisterService(
            uow=mock_uow,
            password_hasher=mock_password_hasher,
            password_policies_suite=mock_password_policy_suite,
            event_publishers=[],
        )

        cmd = RegisterCommand(email=sample_email, password=sample_password)
        result = await service.register(cmd)

        assert isinstance(result, RegisterResult)
        assert result.account.email == sample_email

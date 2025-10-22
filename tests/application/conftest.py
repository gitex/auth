"""Fixtures for application layer tests.

Application tests use mocks for infrastructure dependencies to test
use cases in isolation.
"""

from typing import Any
from unittest.mock import AsyncMock, Mock
from uuid import uuid4

import pytest

from src.domain.entities import Account
from src.domain.events import DomainEvent
from src.domain.policies.password import PasswordPolicySuite
from src.domain.ports import (
    AccountRepository,
    DomainEventPublisher,
    JwtService,
    PasswordHasher,
)
from src.domain.value_objects import (
    AccessToken,
    Email,
    Password,
    PasswordHash,
    RefreshToken,
)

from src.application.uow import UnitOfWork


class MockAccountRepository:
    """Mock implementation of AccountRepository for testing."""

    def __init__(self) -> None:
        self.accounts: dict[str, Account] = {}
        self.get_by_email = AsyncMock(side_effect=self._get_by_email)
        self.get_by_id = AsyncMock(side_effect=self._get_by_id)
        self.create = AsyncMock(side_effect=self._create)
        self.exists = AsyncMock(side_effect=self._exists)

    async def _get_by_email(self, email: Email) -> Account | None:
        return self.accounts.get(email.value)

    async def _get_by_id(self, account_id: Any) -> Account | None:
        for account in self.accounts.values():
            if account.identifier == account_id:
                return account
        return None

    async def _create(self, account: Account) -> Account:
        account.identifier = uuid4()
        self.accounts[account.email.value] = account
        return account

    async def _exists(self, email: Email) -> bool:
        return email.value in self.accounts


class MockUnitOfWork:
    """Mock implementation of UnitOfWork for testing."""

    def __init__(self, accounts: AccountRepository | None = None) -> None:
        self.accounts = accounts or MockAccountRepository()
        self.committed = False
        self.rolled_back = False

    async def __aenter__(self) -> 'MockUnitOfWork':
        return self

    async def __aexit__(self, exc_type: Any, exc: Any, tb: Any) -> None:
        if exc_type:
            await self.rollback()
        else:
            await self.commit()

    async def commit(self) -> None:
        self.committed = True

    async def rollback(self) -> None:
        self.rolled_back = True


class MockPasswordHasher:
    """Mock implementation of PasswordHasher for testing."""

    def __init__(self) -> None:
        self.hash = AsyncMock(side_effect=self._hash)
        self.verify = AsyncMock(side_effect=self._verify)

    async def _hash(self, password: Password) -> PasswordHash:
        return PasswordHash(f'hashed_{password.value}')

    async def _verify(self, password: Password, password_hash: PasswordHash) -> bool:
        expected_hash = f'hashed_{password.value}'
        return password_hash.value == expected_hash


class MockJwtService:
    """Mock implementation of JwtService for testing."""

    def __init__(self) -> None:
        self.issue_access = AsyncMock(side_effect=self._issue_access)
        self.issue_refresh = AsyncMock(side_effect=self._issue_refresh)

    async def _issue_access(self, account: Account, scopes: list) -> AccessToken:
        return AccessToken(f'access_token_for_{account.email.value}')

    async def _issue_refresh(self, account: Account) -> RefreshToken:
        return RefreshToken(f'refresh_token_for_{account.email.value}')


class MockEventPublisher:
    """Mock implementation of DomainEventPublisher for testing."""

    def __init__(self) -> None:
        self.published_events: list[DomainEvent] = []
        self.publish = AsyncMock(side_effect=self._publish)

    async def _publish(self, event: DomainEvent) -> None:
        self.published_events.append(event)


class MockPasswordPolicySuite:
    """Mock implementation of PasswordPolicySuite for testing."""

    def __init__(self, should_pass: bool = True, errors: list[str] | None = None):
        self.should_pass = should_pass
        self.errors = errors or []

    def validate(self, password: Password) -> tuple[bool, list[str]]:
        return (self.should_pass, self.errors)


@pytest.fixture
def mock_account_repository() -> MockAccountRepository:
    """Mock account repository for tests."""
    return MockAccountRepository()


@pytest.fixture
def mock_uow(mock_account_repository: MockAccountRepository) -> MockUnitOfWork:
    """Mock unit of work for tests."""
    return MockUnitOfWork(accounts=mock_account_repository)


@pytest.fixture
def mock_password_hasher() -> MockPasswordHasher:
    """Mock password hasher for tests."""
    return MockPasswordHasher()


@pytest.fixture
def mock_jwt_service() -> MockJwtService:
    """Mock JWT service for tests."""
    return MockJwtService()


@pytest.fixture
def mock_event_publisher() -> MockEventPublisher:
    """Mock event publisher for tests."""
    return MockEventPublisher()


@pytest.fixture
def mock_password_policy_suite() -> MockPasswordPolicySuite:
    """Mock password policy suite that always passes."""
    return MockPasswordPolicySuite(should_pass=True)


@pytest.fixture
def sample_email() -> Email:
    """Sample Email value object for tests."""
    return Email('test@example.com')


@pytest.fixture
def sample_password() -> Password:
    """Sample Password value object for tests."""
    return Password('Test@Pass123')


@pytest.fixture
def sample_account(sample_email: Email) -> Account:
    """Sample Account entity for tests."""
    return Account(
        identifier=uuid4(),
        email=sample_email,
        password_hash=PasswordHash('hashed_Test@Pass123'),
        is_active=True,
    )

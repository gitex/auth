import typing as tp
from datetime import UTC, datetime

from pydantic import BaseModel, Field

from src.domain.value_objects import Email


class DomainEvent(BaseModel):
    occurred_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    def as_dict(self) -> dict[str, tp.Any]:
        return self.model_dump()


class AccountRegistered(DomainEvent):
    email: Email

    @classmethod
    def from_account(cls, account: 'Account') -> 'AccountRegistered':
        from src.domain.entities import Account

        return cls(email=account.email)


class AccountAuthorized(DomainEvent):
    email: Email


class AccountForgotPassword(DomainEvent):
    email: Email


class AccountPasswordChanged(DomainEvent):
    """Domain event emitted when account password is changed."""

    email: Email


class AccountActivated(DomainEvent):
    """Domain event emitted when account is activated."""

    email: Email


class AccountDeactivated(DomainEvent):
    """Domain event emitted when account is deactivated."""

    email: Email

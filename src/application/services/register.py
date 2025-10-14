from dataclasses import dataclass, field

from src.domain.entities import Account
from src.domain.events import UserRegistered
from src.domain.policies.password import PasswordPolicy
from src.domain.ports import DomainEventPublisher, PasswordHasher
from src.domain.value_objects import Email, Password

from src.application.exceptions import (
    AccountAlreadyExistsError,
    PasswordPolicyError,
)
from src.application.uow import UnitOfWork


@dataclass(frozen=True, slots=True)
class RegisterCommand:
    email: Email
    password: Password


@dataclass
class RegisterResult:
    account: Account


@dataclass
class RegisterService:
    uow: UnitOfWork
    password_hasher: PasswordHasher
    password_policy: PasswordPolicy
    event_publishers: list[DomainEventPublisher] = field(default_factory=list)

    async def register(self, cmd: RegisterCommand) -> RegisterResult:
        async with self.uow as uow:
            account = await uow.accounts.get_by_email(cmd.email)

        if account:
            raise AccountAlreadyExistsError(ctx={'email': cmd.email})

        ok, errors = self.password_policy.validate(cmd.password)
        if not ok:
            raise PasswordPolicyError(ctx={'errors': errors})

        async with self.uow as uow:
            account = await uow.accounts.create(
                Account(
                    identifier=None,
                    username=None,
                    email=cmd.email,
                    password_hash=await self.password_hasher.hash(cmd.password),
                    is_active=True,
                    roles=[],  # TODO: Обновить после добавления ролей
                )
            )

            event = UserRegistered(
                user_id=account.identifier,
                email=account.email,
            )

            for event_publisher in self.event_publishers:
                await event_publisher.publish(event)

        return RegisterResult(account=account)

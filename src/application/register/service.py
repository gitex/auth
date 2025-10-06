from dataclasses import dataclass

from src.domain.entities import Account
from src.domain.policies.password import PasswordPolicy
from src.domain.ports import PasswordHasher
from src.domain.value_objects import Email, Password

from src.infra.crypto.bcrypt import BcryptPasswordHasherImpl

from src.application.exceptions import (
    AccountAlreadyExistsError,
    PasswordPolicyError,
)
from src.application.session import SessionFactory
from src.application.uow import SqlAlchemyUoW, UnitOfWork


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

    async def register(self, cmd: RegisterCommand) -> RegisterResult:
        async with self.uow as uow:
            account = await uow.accounts.get_by_email(cmd.email)

        if account:
            raise AccountAlreadyExistsError({"email": cmd.email})

        ok, errors = self.password_policy.validate(cmd.password)
        if not ok:
            raise PasswordPolicyError({"errors": errors})

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

        return RegisterResult(account=account)


def get_register_service() -> RegisterService:
    return RegisterService(
        uow=SqlAlchemyUoW(SessionFactory),
        password_hasher=BcryptPasswordHasherImpl(),
        password_policy=PasswordPolicy(
            min_length=4,
            require_symbols=False,
            require_digit=False,
        ),
    )

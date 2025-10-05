from dataclasses import dataclass

from src.domain.entities import Account
from src.domain.exceptions import InvalidCredentialsError
from src.domain.policies.password import PasswordPolicy
from src.domain.ports import AccountRepository, JwtService, PasswordHasher
from src.domain.value_objects import AccessToken, Email, Password, RefreshToken


INVALID_CREDENTIALS_MESSAGE = "Invalid credentials"


@dataclass
class LoginResult:
    access_token: AccessToken
    refresh_token: RefreshToken


@dataclass
class LoginService:
    repository: AccountRepository
    password_hasher: PasswordHasher
    jwt_service: JwtService

    async def login(self, email: Email, password: Password) -> LoginResult:
        account = await self.repository.get_by_email(email)

        if not account:
            raise InvalidCredentialsError(INVALID_CREDENTIALS_MESSAGE)

        if not await self.password_hasher.verify(password, account.password_hash):
            raise InvalidCredentialsError(INVALID_CREDENTIALS_MESSAGE)

        access_token = await self.jwt_service.issue_access(account, scopes=[])
        refresh_token = await self.jwt_service.issue_refresh(account)

        return LoginResult(access_token, refresh_token)


@dataclass
class RegisterService:
    password_policy: PasswordPolicy
    password_hasher: PasswordHasher
    repository: AccountRepository

    async def register(self, email: Email, password: Password) -> Account:
        errors = self.password_policy.validate(password)

        if errors:
            ...  # TODO: Непонятно что тут делать и как передавать ошибки дальше

        password_hash = await self.password_hasher.hash(password)

        account = Account(id=None, email=email, password_hash=password_hash, roles=[])
        account = await self.repository.create(account)
        return account

from dataclasses import dataclass

from src.domain.exceptions import InvalidCredentialsError
from src.domain.ports import AccountRepository, JwtService, PasswordHasher
from src.domain.value_objects import AccessToken, RefreshToken


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

    async def login(self, email: str, plain_password: str) -> LoginResult:
        account = await self.repository.get_by_email(email)

        if not account:
            raise InvalidCredentialsError(INVALID_CREDENTIALS_MESSAGE)

        if not await self.password_hasher.verify(plain_password, account.password_hash):
            raise InvalidCredentialsError(INVALID_CREDENTIALS_MESSAGE)

        access_token = await self.jwt_service.issue_access(account, scopes=["auth"])
        refresh_token = await self.jwt_service.issue_refresh(account)

        return LoginResult(access_token, refresh_token)

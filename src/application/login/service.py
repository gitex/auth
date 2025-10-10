from dataclasses import dataclass

from src.domain.ports import JwtService, PasswordHasher
from src.domain.value_objects import AccessToken, Email, Password, RefreshToken

from src.application.exceptions import InvalidCredentialsError
from src.application.uow import UnitOfWork


@dataclass
class LoginResult:
    access_token: AccessToken
    refresh_token: RefreshToken


@dataclass(frozen=True)
class LoginService:
    uow: UnitOfWork
    password_hasher: PasswordHasher
    jwt_service: JwtService

    async def login(self, email: Email, password: Password) -> LoginResult:
        """Авторизует пользователя.

        :raise InvalidCredentialsError:
        :raise InvalidClaimsError:
        """
        async with self.uow as uow:
            account = await uow.accounts.get_by_email(email)

        if not account or not await self.password_hasher.verify(
            password, account.password_hash
        ):
            raise InvalidCredentialsError({'email': email})

        access_token = await self.jwt_service.issue_access(account, scopes=[])
        refresh_token = await self.jwt_service.issue_refresh(account)

        return LoginResult(access_token, refresh_token)

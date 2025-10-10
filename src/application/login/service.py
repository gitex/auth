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
        """
        Authorize user from email and password.

        Args:
            email: User email
            password: User password

        Returns:
            Access and refresh token

        Raises:
            InvalidCredentialsError: Email or password is not valid
        """

        async with self.uow as uow:
            account = await uow.accounts.get_by_email(email)

        if not account:
            raise InvalidCredentialsError('Account does not found', ctx={'email': email})

        if not await self.password_hasher.verify(password, account.password_hash):
            raise InvalidCredentialsError('Incorrect password', ctx={'email': email})

        access_token = await self.jwt_service.issue_access(account, scopes=[])
        refresh_token = await self.jwt_service.issue_refresh(account)

        return LoginResult(access_token, refresh_token)

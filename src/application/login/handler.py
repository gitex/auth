from dataclasses import dataclass

from infra.claims.policies import TokenPolicy
from infra.jwt_service.jose import JoseJwtServiceImpl
from src.application.uow import SqlAlchemyUoW, UnitOfWork
from src.domain.exceptions import InvalidCredentialsError
from src.domain.ports import JwtService, PasswordHasher
from src.domain.value_objects import AccessToken, Email, Password, RefreshToken
from src.infra.config import settings
from src.infra.crypto.bcrypt import BcryptPasswordHasherImpl


INVALID_CREDENTIALS_MESSAGE = "Invalid credentials"


@dataclass
class LoginResult:
    access_token: AccessToken
    refresh_token: RefreshToken


@dataclass(frozen=True)
class LoginHandler:
    uow: UnitOfWork
    password_hasher: PasswordHasher
    jwt_service: JwtService

    async def login(self, email: Email, password: Password) -> LoginResult:
        async with self.uow as uow:
            account = await uow.account_repository.get_by_email(email)

        if not account:
            raise InvalidCredentialsError(INVALID_CREDENTIALS_MESSAGE)

        if not await self.password_hasher.verify(password, account.password_hash):
            raise InvalidCredentialsError(INVALID_CREDENTIALS_MESSAGE)

        access_token = await self.jwt_service.issue_access(account, scopes=[])
        refresh_token = await self.jwt_service.issue_refresh(account)

        return LoginResult(access_token, refresh_token)


def get_login_handler(session_factory) -> LoginHandler:  # TODO: Нужен ли DI?
    return LoginHandler(
        uow=SqlAlchemyUoW(session_factory),
        password_hasher=BcryptPasswordHasherImpl(),
        jwt_service=JoseJwtServiceImpl(
            secret=settings.jwt.secret_key.get_secret_value(),
            policy=TokenPolicy(
                settings.jwt.issuer,
                settings.jwt.audience,
            ),
        ),
    )

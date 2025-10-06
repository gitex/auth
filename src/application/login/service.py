from dataclasses import dataclass
from datetime import timedelta

from src.domain.ports import JwtService, PasswordHasher
from src.domain.value_objects import AccessToken, Email, Password, RefreshToken

from src.infra.claims.policies import TokenPolicy
from src.infra.config import settings
from src.infra.crypto.bcrypt import BcryptPasswordHasherImpl
from src.infra.jwt_service.jose import JoseJwtServiceImpl

from src.application.exceptions import InvalidCredentialsError
from src.application.session import SessionFactory
from src.application.uow import SqlAlchemyUoW, UnitOfWork


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
            raise InvalidCredentialsError({"email": email})

        access_token = await self.jwt_service.issue_access(account, scopes=[])
        refresh_token = await self.jwt_service.issue_refresh(account)

        return LoginResult(access_token, refresh_token)


def get_login_service() -> LoginService:  # TODO: Нужен ли DI?
    return LoginService(
        uow=SqlAlchemyUoW(SessionFactory),
        password_hasher=BcryptPasswordHasherImpl(),
        jwt_service=JoseJwtServiceImpl(
            secret=settings.jwt.secret_key.get_secret_value(),
            policy=TokenPolicy(  # TODO: Передать алгоритм с настроек
                settings.jwt.issuer,
                settings.jwt.audience,
                access_ttl=timedelta(seconds=settings.jwt.access_ttl_seconds),
                refresh_ttl=timedelta(seconds=settings.jwt.refresh_ttl_seconds),
            ),
        ),
    )

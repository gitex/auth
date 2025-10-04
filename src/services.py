from collections.abc import Callable
from dataclasses import dataclass

from src.auth_types import Token
from src.claims import Claims, ClaimsFactory, PrivateClaims
from src.codecs.base import JwtCodec
from src.dto import JwtSpec
from src.exceptions import InvalidCredentials
from src.password_helper.base import PasswordHelper
from src.repositories.base import AccountRepository
from src.storage.base import RefreshStore


@dataclass
class Tokens:
    access_token: Token
    refresh_token: Token


TYP_ACCESS = "access"
TYP_REFRESH = "refresh"


@dataclass(frozen=True)
class TokenFactory:
    jwt_codec: JwtCodec
    claims_factory: ClaimsFactory
    validate_claims: Callable[[Claims], bool] = lambda _: True  # TODO: Protocol, default

    def generate(self, sub: str, custom_claims: PrivateClaims) -> Tokens:
        # claims_factory = ClaimsFactory(jwt_spec=self.jwt_spec)
        access_claims = self.claims_factory.access_claims(
            sub, custom_claims=custom_claims
        )
        refresh_claims = self.claims_factory.refresh_claims(sub)

        self.validate_claims(access_claims)
        self.validate_claims(refresh_claims)

        access_token = self.jwt_codec.encode(access_claims)
        refresh_token = self.jwt_codec.encode(refresh_claims)

        return Tokens(access_token=access_token, refresh_token=refresh_token)


@dataclass(frozen=True)
class AuthService:
    repository: AccountRepository
    jwt_codec: JwtCodec
    jwt_spec: JwtSpec
    password_helper: PasswordHelper
    token_factory: TokenFactory
    refresh_store: RefreshStore | None = None

    async def login(self, email: str, password: str) -> Tokens:
        account = await self.repository.get_by_email(email)

        if not account:
            raise InvalidCredentials("Invalid credentials")

        if not await self.password_helper.verify(password, account.password_hash):
            raise InvalidCredentials("Invalid credentials")

        tokens = self.token_factory.generate(
            sub=account.id.hex, custom_claims=PrivateClaims(email=account.email)
        )

        # self.refresh_store.save()

        return tokens

    async def refresh_tokens(self, token: Token) -> Tokens: ...

    async def logout(self, refresh_token: Token) -> None: ...

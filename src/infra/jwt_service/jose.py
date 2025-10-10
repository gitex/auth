from dataclasses import dataclass

from jose import jwt

from src.domain.entities import Account
from src.domain.factories import ClaimsFactory
from src.domain.ports import JwtService
from src.domain.value_objects import AccessToken, Claims, RefreshToken, Scope

from src.infra.key_provider import KeyProvider


@dataclass(frozen=True, slots=True)
class JoseJwtServiceImpl(JwtService):
    """Сервис создания и валидации токенов."""

    claims_factory: ClaimsFactory
    key_provider: KeyProvider

    async def _encode_claims(self, claims: Claims) -> str:
        return jwt.encode(
            claims.as_dict(),
            self.key_provider.signing_key(),
            algorithm=self.key_provider.algorithm(),
        )

    async def issue_access(self, account: Account, scopes: list[Scope]) -> AccessToken:
        claims = self.claims_factory.access_claims(sub=str(account.identifier))
        token = await self._encode_claims(claims)
        return AccessToken(token)

    async def issue_refresh(self, account: Account) -> RefreshToken:
        claims = self.claims_factory.refresh_claims(sub=str(account.identifier))
        token: str = await self._encode_claims(claims)
        return RefreshToken(token)

    async def verify_access(self, access_token: AccessToken) -> Account | None: ...

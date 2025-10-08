from jose import jwt

from src.domain.entities import Account
from src.domain.ports import JwtService
from src.domain.value_objects import AccessToken, RefreshToken, Scope

from src.infra.claims import Claims, ClaimsFactory, TokenPolicy
from src.infra.exceptions import InvalidClaimsError


class JoseJwtServiceImpl(JwtService):
    def __init__(self, secret: str, policy: TokenPolicy) -> None:
        self._secret = secret
        self._policy = policy

    async def _encode_claims(self, claims: Claims) -> str:
        return jwt.encode(
            claims.as_dict(),
            self._secret,
            algorithm=self._policy.algorithm,
        )

    def _validate(self, claims: Claims) -> None:
        ok, errors = self._policy.validate(claims)
        if not ok:
            raise InvalidClaimsError({'errors': errors})

    async def issue_access(self, account: Account, scopes: list[Scope]) -> AccessToken:
        claims_factory = ClaimsFactory(policy=self._policy)
        claims = claims_factory.access_claims(sub=str(account.identifier))
        self._validate(claims)
        token = await self._encode_claims(claims)
        return AccessToken(token)

    async def issue_refresh(self, account: Account) -> RefreshToken:
        claims_factory = ClaimsFactory(policy=self._policy)
        claims = claims_factory.refresh_claims(sub=str(account.identifier))
        self._validate(claims)
        token: str = await self._encode_claims(claims)
        return RefreshToken(token)

    async def verify_access(self, access_token: AccessToken) -> Account | None: ...

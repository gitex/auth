from typing import Any, override

from antidote import implements
from jose import jwt

from src.auth_types import Algorithm
from src.infra.claims.entities import Claims

from .base import JwtCodec, Token


@implements(JwtCodec).as_default
class JoseJwtCodec(JwtCodec):
    """Реализация encode/decode для jose."""

    def __init__(self, secret: str, algorithm: Algorithm) -> None:
        self._secret = secret
        self._algorithm = algorithm

    @override
    def encode(self, claims: Claims) -> Token:
        return jwt.encode(
            claims.as_dict(),
            self._secret,
            algorithm=self._algorithm,
        )

    @override
    def decode(self, token: Token, audience: str | None = None) -> Claims:
        payload: dict[str, Any] = jwt.decode(
            token,
            key=self._secret,
            algorithms=[self._algorithm],
            audience=audience,
            options={
                "verify_signature": True,
            },
        )

        return Claims.model_validate(payload)

from enum import StrEnum
from typing import Protocol


class JwtAlgorithm(StrEnum):
    HS256 = 'HS256'


class KeyProvider(Protocol):
    def algorithm(self) -> str: ...
    def current_kid(self) -> str | None: ...
    def signing_key(self) -> str: ...
    def verification_key(self, kid: str | None) -> str: ...


class HS256KeyProviderImpl(KeyProvider):
    def __init__(self, secret: str) -> None:
        self._secret = secret

    def algorithm(self) -> str:
        return JwtAlgorithm.HS256.value

    def current_kid(self) -> str | None:
        return None

    def signing_key(self) -> str:
        return self._secret

    def verification_key(self, kid: str | None) -> str:
        return self._secret

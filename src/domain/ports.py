from datetime import datetime
from typing import Protocol
from uuid import UUID

from src.domain.value_objects import (
    TTL,
    AccessToken,
    Email,
    Password,
    PasswordHash,
    RefreshFamilyId,
    RefreshSessionId,
    RefreshToken,
    Scope,
)

from .entities import Account


class Clock(Protocol):
    def now(self) -> datetime: ...
    def now_ts(self) -> int: ...


class RefreshStore(Protocol):
    async def save(self, refresh_token: RefreshToken) -> None: ...
    async def get(self, refresh_id: RefreshSessionId) -> RefreshToken | None: ...
    async def rotate(self, old: RefreshToken, new: RefreshToken) -> None: ...


class RevokeStore(Protocol):
    async def is_revoked(self, refresh_id: RefreshSessionId) -> bool: ...
    async def revoke(self, refresh_id: RefreshSessionId, ttl: TTL) -> None: ...
    async def delete_family(self, family: RefreshFamilyId) -> None: ...


class JwtService(Protocol):
    async def issue_access(
        self, account: Account, scopes: list[Scope]
    ) -> AccessToken: ...
    async def issue_refresh(self, account: Account) -> RefreshToken: ...


class PasswordHasher(Protocol):
    async def hash(self, password: Password) -> PasswordHash: ...
    async def verify(self, password: Password, password_hash: PasswordHash) -> bool: ...


class AccountRepository(Protocol):
    async def get_by_email(self, email: Email) -> Account | None: ...
    async def get_by_id(self, account_id: UUID) -> Account | None: ...
    async def create(self, account: Account) -> Account: ...

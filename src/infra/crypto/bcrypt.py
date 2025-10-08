from typing import override

from passlib.context import CryptContext

from src.domain.ports import PasswordHasher
from src.domain.value_objects import Password, PasswordHash


class BcryptPasswordHasherImpl(PasswordHasher):
    def __init__(self) -> None:
        self._context: CryptContext = CryptContext(
            schemes=["argon2"],
            deprecated="auto",
            argon2__time_cost=3,
            argon2__memory_cost=64_000,
            argon2__parallelism=1,
        )

    @override
    async def verify(self, password: Password, password_hash: PasswordHash) -> bool:
        return self._context.verify(password.value, password_hash.value)

    @override
    async def hash(self, password: Password) -> PasswordHash:
        return PasswordHash(self._context.hash(password.value))

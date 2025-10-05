from typing import override

from passlib.context import CryptContext
from passlib.hash import bcrypt

from src.domain.ports import PasswordHasher
from src.domain.value_objects import Password, PasswordHash


class BcryptPasswordHasherImpl(PasswordHasher):
    def __init__(self) -> None:
        self._context: CryptContext = CryptContext(schemes=["bcrypt"], deprecated="auto")

    @override
    async def verify(self, password: Password, password_hash: PasswordHash) -> bool:
        return bcrypt.verify(password.value, password_hash.value)

    @override
    async def hash(self, password: Password) -> PasswordHash:
        return PasswordHash(self._context.hash(password.value))

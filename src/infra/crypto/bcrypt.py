from typing import override

from passlib.context import CryptContext
from passlib.hash import bcrypt

from src.domain.ports import PasswordHasher


class BcryptPasswordHasher(PasswordHasher):
    def __init__(self) -> None:
        self._context: CryptContext = CryptContext(schemes=["bcrypt"], deprecated="auto")

    @override
    async def verify(self, password: str, password_hash: str) -> bool:
        return bcrypt.verify(password, password_hash)

    @override
    async def hash(self, password: str) -> str:
        return self._context.hash(password)

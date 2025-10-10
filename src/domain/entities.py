from dataclasses import dataclass, field
from uuid import UUID

from src.domain.value_objects import Email, PasswordHash, Role


@dataclass
class Account:
    identifier: UUID | None
    email: Email
    password_hash: PasswordHash
    is_active: bool = True
    username: str | None = field(default=None)
    roles: list[Role] = field(default_factory=list)

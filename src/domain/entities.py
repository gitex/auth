from dataclasses import dataclass, field
from uuid import UUID

from src.domain.value_objects import Email, PasswordHash, Role


@dataclass
class PrivateClaims:
    """
    Attributes:
        email: email клиента
        roles: Роли клиента
        scope: Набор сервисов, для которых token валиден
        groups: Список групп прав пользователя
    """

    email: str | None = None
    roles: list[str] | None = None
    scope: str | None = None
    groups: list[str] | None = None


@dataclass
class Account:
    identifier: UUID | None
    email: Email
    password_hash: PasswordHash
    is_active: bool = True
    username: str | None = field(default=None)
    roles: list[Role] = field(default_factory=list)

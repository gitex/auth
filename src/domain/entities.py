from dataclasses import dataclass, field
from uuid import UUID


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
    id: UUID
    email: str
    password_hash: str
    is_active: bool = True
    roles: list[str] = field(default_factory=list)

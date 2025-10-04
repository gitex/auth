from dataclasses import dataclass

from src.domain.value_objects import TTL, Email, Role, Scope


@dataclass
class Principal:
    """Представление клиента.

    Attributes:
        sub: (subject) Идентификатор клиента
        roles: Роли клиента
        scopes: Права клиента
    """

    sub: str
    email: Email
    roles: set[Role]
    scopes: set[Scope]


@dataclass
class JwtSpec:
    """

    Attributes:
        alg: Алгоритм шифрования
        iss: (Issuer): кто выдал токен?
        aud: (Audience): для каких сервисов он валиден?
    """

    alg: AlgorithmStr
    secret: str
    iss: str
    aud: str
    access_ttl: TTL
    refresh_ttl: TTL

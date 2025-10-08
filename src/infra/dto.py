from dataclasses import dataclass

from src.domain.value_objects import TTL


@dataclass
class JwtSpec:
    """Attributes:
    alg: Алгоритм шифрования
    iss: (Issuer): кто выдал токен?
    aud: (Audience): для каких сервисов он валиден?
    """

    alg: str
    secret: str
    iss: str
    aud: str
    access_ttl: TTL
    refresh_ttl: TTL

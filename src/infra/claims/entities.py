from dataclasses import asdict, dataclass
from typing import Any, Self

from src.domain.entities import PrivateClaims

from .value_objects import Timestamp


@dataclass
class _BaseClaims:
    def as_dict(self, exclude_none: bool = False) -> dict[str, Any]:
        """Возвращает значения в dict, пропуская отсутствующие (необязательные) значения.

        Необходимо всегда формировать claims через этот метод, чтобы была возможность
        отвязаться от pydanctic.
        """

        output = {}

        for key, value in asdict(self).items():
            if exclude_none and value is None:
                continue
            output[key] = value

        return output

    def update(self, other: "_BaseClaims") -> Self:
        """Обновляет значения из других Claims."""

        for key, value in asdict(other).items():
            setattr(self, key, value)

        return self


@dataclass
class RegisteredClaims:
    """Официальные claims для токена.

    https://datatracker.ietf.org/doc/html/rfc7519#section-4.1

    Attributes:
        sub: (Subject) - Client Identifier
        iss: (Issuer) - Кто выдал токен?
        aud: (Audience) - Для каких сервисов выдал?
        exp: (Expiration Time) - Unix время истечения токена
        nbf: (Not Before) - Unix время начала работы токена
        iat: (Issued at) - Unix время выпуска токена
        jti: (JWT ID) - Уникальный идентификатор самого токена

    Важно: по спецификации все значения - опциональны (да, даже exp).
    Именно поэтому они все указаны None.
    """

    sub: str | None = None
    iss: str | None = None
    aud: str | None = None
    exp: Timestamp | None = None
    nbf: Timestamp | None = None
    iat: Timestamp | None = None
    jti: str | None = None


@dataclass
class Claims(PrivateClaims, RegisteredClaims):
    def as_dict(self) -> dict:
        return asdict(self)

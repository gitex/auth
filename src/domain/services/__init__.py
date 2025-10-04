class PasswordPolicy:
    """Политика длины, состава, истории, срока жизни пароля."""

    def verify(self, plain_password: str) -> bool: ...


class LockoutPolicy:
    """N неуспешных попыток -> блокировка по времени."""


class TokenPolicy:
    """TTL, состав claims, audience/issuer, clock-skew."""


class RefreshRotationService:
    """Атомарная ротация, защина от переиспользования."""

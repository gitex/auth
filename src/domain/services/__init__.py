class LockoutPolicy:
    """N неуспешных попыток -> блокировка по времени."""


class TokenPolicy:
    """TTL, состав claims, audience/issuer, clock-skew."""


class RefreshRotationService:
    """Атомарная ротация, защина от переиспользования."""

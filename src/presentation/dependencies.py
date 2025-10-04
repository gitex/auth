from datetime import timedelta

from antidote import inject, lazy

from src.config import Settings
from src.dto import JwtSpec


@lazy
def get_jwt_spec(settings: Settings = inject.me()) -> JwtSpec:
    return JwtSpec(
        alg=settings.jwt.alg,
        secret=settings.jwt.secret_key,
        iss=settings.jwt.iss,
        aud=settings.jwt.aud,
        access_ttl=timedelta(seconds=settings.jwt.access_ttl_seconds),
        refresh_ttl=timedelta(seconds=settings.jwt.refresh_ttl_seconds),
    )

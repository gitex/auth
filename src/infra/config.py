from datetime import timedelta

from antidote import injectable
from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Jwt(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="JWT_")

    alg: str = "HS256"
    secret_key: SecretStr = SecretStr(
        "Az8H28hPZ25uTCg67BOQRj1KnCiXfJV2pYoQ8bsLVuxVl3JVh16"
    )
    audience: str = "auth"
    issuer: str = "auth"
    access_ttl_seconds: int = 60 * 15  # 15 minutes
    refresh_ttl_seconds: int = 60 * 60 * 24  # 1 day

    @property
    def access_ttl(self) -> timedelta:
        return timedelta(seconds=self.access_ttl_seconds)

    @property
    def refresh_ttl(self) -> timedelta:
        return timedelta(seconds=self.refresh_ttl_seconds)


@injectable
class Settings(BaseSettings):
    model_config = SettingsConfigDict()

    debug: bool = True
    app_name: str = "auth"
    database_url: str

    jwt: Jwt = Jwt()


# Some settings do not have defaults, because it's user's responsibility for
#   setting these values. Errors would be a signal of necessity and importance those settings.
#   Default settings for database and other important stuff can create confusion for developer.
settings = Settings()  # type: ignore [call-arg]

from dependency_injector import containers, providers

from src.domain.factories.claims import ClaimsFactory
from src.domain.policies.password import PasswordPolicy
from src.domain.value_objects.token import TokenLifetime, TokenRealm, TokenSpecification

from src.infra.config import Settings
from src.infra.crypto.bcrypt import BcryptPasswordHasherImpl
from src.infra.jwt_service.jose import JoseJwtServiceImpl
from src.infra.key_provider import HS256KeyProviderImpl
from src.infra.orm.session import make_async_session_factory, make_engine

from src.application import LoginService, RegisterService, SqlAlchemyUoW


class AuthContainer(containers.DeclarativeContainer):
    config = providers.Configuration(pydantic_settings=[Settings()])  # type: ignore [call-arg]

    engine = providers.Singleton(
        make_engine,
        url=config.database_url.required(),
        echo=config.debug,
    )
    session_factory = providers.Singleton(
        make_async_session_factory,
        engine=engine,
    )

    uow = providers.Factory(
        SqlAlchemyUoW,
        session_factory=session_factory,
    )

    password_hasher = providers.Factory(
        BcryptPasswordHasherImpl,
    )

    key_provider = providers.Factory(
        HS256KeyProviderImpl,
        secret=config.jwt.secret_key.provided.get_secret_value.call(),  # SecretStr
    )

    token_specification = providers.Factory(
        TokenSpecification,
        realm=providers.Factory(
            TokenRealm,
            issuer=config.jwt.issuer.required(),
            audience=config.jwt.audience.required(),
        ),
        lifetime=providers.Factory(
            TokenLifetime,
            access_ttl=config.jwt.access_ttl.required(),
            refresh_ttl=config.jwt.refresh_ttl.required(),
            clock_skew=config.jwt.clock_skew.required(),
        ),
    )

    claims_factory = providers.Factory(
        ClaimsFactory,
        spec=token_specification,
    )

    jwt_service = providers.Factory(
        JoseJwtServiceImpl,
        key_provider=key_provider,
        claims_factory=claims_factory,
    )

    login_service = providers.Factory(
        LoginService,
        uow=uow,
        password_hasher=password_hasher,
        jwt_service=jwt_service,
    )

    password_policy = providers.Singleton(
        PasswordPolicy,
        min_length=6,
        require_digit=False,
        require_upper=False,
        require_symbol=False,
    )

    register_service = providers.Factory(
        RegisterService,
        uow=uow,
        password_hasher=password_hasher,
        password_policy=password_policy,
    )

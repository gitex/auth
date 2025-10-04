from src.domain.services.login import LoginService
from src.infra.crypto.bcrypt import BcryptPasswordHasher


class AuthHandler:
    def login(email: str, password: str):
        service = LoginService(
            repository=None,
            password_hasher=BcryptPasswordHasher(),
            jwt_service=None,
        )

        return service.login(email, password)

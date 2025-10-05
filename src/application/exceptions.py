from src.exceptions import AuthError


class ApplicationError(AuthError): ...  # Ошибка уровня application/


class SessionNotFoundError(ApplicationError): ...

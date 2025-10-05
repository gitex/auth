class ApplicationError(Exception): ...  # TODO: вынести в core


class AuthError(ApplicationError): ...  # Ошибка уровня сервиса


class ConfigurationError(AuthError): ...

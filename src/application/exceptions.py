from src.exceptions import MicroserviceError


class ApplicationError(MicroserviceError): ...  # Ошибка уровня application/


class InvalidCredentialsError(ApplicationError):
    code = "invalid_credentials"
    message = "Email or password not valid."


class AccountAlreadyExistsError(ApplicationError):
    code = "account_already_exists"
    message = "Account with this email already registered."


class PasswordPolicyError(ApplicationError):
    code = "password_policy_error"
    message = "Password does not comply with policy."

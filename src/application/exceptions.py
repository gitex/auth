from src.exceptions import BaseMicroserviceError


class BaseApplicationError(BaseMicroserviceError): ...  # Ошибка уровня application/


class InvalidCredentialsError(BaseApplicationError):
    code = 'invalid_credentials'
    message = 'Email or password not valid.'


class AccountAlreadyExistsError(BaseApplicationError):
    code = 'account_already_exists'
    message = 'Account with this email already registered.'


class PasswordPolicyError(BaseApplicationError):
    code = 'password_policy_error'
    message = 'Password does not comply with policy.'

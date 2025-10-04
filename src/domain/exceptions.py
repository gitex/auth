class ApplicationError(Exception):
    """Base exception for inheritance.

    Do not call this error directly. Make errors for specific cases.
    """


class ValidationError(ApplicationError): ...


class AuthError(ApplicationError): ...  # базовый Exception


class InvalidCredentialsError(AuthError): ...


class JwtError(ApplicationError): ...


class ClaimError(JwtError): ...


class InsufficientScopeError(JwtError): ...

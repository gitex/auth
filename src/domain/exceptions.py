from src.exceptions import MicroserviceError


class DomainError(MicroserviceError): ...


class ValidationError(DomainError):
    code = 'validation_error'
    message = 'Invalid value'


class ShouldBePositiveError(ValidationError):
    code = 'value_should_be_positive'
    message = 'Value should be positive'


class InvalidCredentialsError(DomainError):
    code = 'invalid_credentials'
    message = 'Invalid credentials'

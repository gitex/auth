from src.exceptions import BaseMicroserviceError


class BaseDomainError(BaseMicroserviceError): ...


class ValidationError(BaseDomainError):
    code = 'validation_error'
    message = 'Expected different value'


class ShouldBePositiveError(ValidationError):
    code = 'value_should_be_positive'
    message = 'Value should be positive'

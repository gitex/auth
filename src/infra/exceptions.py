from src.exceptions import BaseMicroserviceError


class BaseInfrastructureError(BaseMicroserviceError): ...


class InvalidClaimsError(BaseInfrastructureError):
    code = 'invalid_claims'
    message = 'Claims are not valid'

from src.exceptions import MicroserviceError


class InfrastructureError(MicroserviceError): ...


class InvalidClaimsError(InfrastructureError):
    code = "invalid_claims"
    message = "Presented claims are not valid"

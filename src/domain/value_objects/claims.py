from dataclasses import asdict, dataclass
from typing import Any

from .account import Role


@dataclass(frozen=True)
class PrivateClaims:
    """Attributes:
    email: User email
    roles: User roles
    scope: Services
    """

    email: str | None = None
    roles: list[Role] | None = None
    scope: str | None = None


@dataclass(frozen=True)
class RegisteredClaims:
    """Official token claims.

    https://datatracker.ietf.org/doc/html/rfc7519#section-4.1

    Attributes:
        sub: (Subject) - Client Identifier
        iss: (Issuer)
        aud: (Audience)
        iat: (Issued at) - Token release time (Unix)
        nbf: (Not Before) - Start of token lifetime (Unix)
        exp: (Expiration Time) - End of token lifetime (Unix)
        jti: (JWT ID) - Unique token identifier

    Important to know: by specification - every claim is optional
    """

    sub: str | None = None
    iss: str | None = None
    aud: list[str] | None = None
    exp: int | None = None
    nbf: int | None = None
    iat: int | None = None
    jti: str | None = None


@dataclass(frozen=True, slots=True)
class Claims(PrivateClaims, RegisteredClaims):
    def as_dict(self, *, exclude_none: bool = False) -> dict[str, Any]:
        """Form dict and exclude empty claims."""
        output = {}

        for key, value in asdict(self).items():
            if exclude_none and value is None:
                continue

            output[key] = value

        return output

from enum import StrEnum


class TokenError(StrEnum):
    REQUIRED_SUB = "required_sub"
    REQUIRED_JTI = "required_jti"
    REQUIRED_EXP = "required_exp"
    WRONG_ISSUER = "wrong_issuer"
    WRONG_AUDIENCE = "wrong_audience"

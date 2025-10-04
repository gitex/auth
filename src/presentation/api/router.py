from fastapi import APIRouter
from pydantic import BaseModel, EmailStr, SecretStr

from services import AuthService
from src.codecs import JoseJwtCodec
from src.dependencies import get_jwt_spec
from src.password_helper import BcryptPasswordHelper
from src.repositories import DBAccountRepository
from src.schemas import TokensOut


router = APIRouter(prefix="/auth", tags=["authorization"])


class LoginIn(BaseModel):
    email: EmailStr
    password: SecretStr


@router.post("/login", response_model=TokensOut)
async def login(body: LoginIn):
    service = AuthService(
        repository=DBAccountRepository(),
        jwt_codec=JoseJwtCodec("test", get_jwt_spec().alg),
        jwt_spec=get_jwt_spec(),
        password_helper=BcryptPasswordHelper(),
    )

    tokens = service.login(body.email, body.password.get_secret_value())

    return TokensOut(
        access_token=tokens.access_token,
        refresh_token=tokens.refresh_token,
    )

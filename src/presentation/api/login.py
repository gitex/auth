from dependency_injector.wiring import inject
from fastapi import APIRouter
from pydantic import BaseModel, EmailStr, SecretStr

from src.domain.value_objects import Email, Password

from src.presentation.dependencies import LoginServiceDepend


router = APIRouter(tags=["authorization"])


class LoginIn(BaseModel):
    email: EmailStr
    password: SecretStr


class LoginOut(BaseModel):
    access_token: str
    refresh_token: str


@router.post("/login")
@inject
async def login(
    body: LoginIn,
    service: LoginServiceDepend,
) -> LoginOut:
    # try:
    result = await service.login(
        email=Email(body.email),
        password=Password(body.password.get_secret_value()),
    )
    # except InvalidCredentialsError:
    #     raise HTTPExceptioj(
    #         status_code=status.HTTP_400_BAD_REQUEST,
    #         detail="Invalid credentials",
    #     )

    return LoginOut(
        access_token=str(result.access_token),
        refresh_token=str(result.refresh_token),
    )

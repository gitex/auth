from dependency_injector.wiring import inject
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, EmailStr, SecretStr

from src.domain.value_objects import Email, Password

from src.application.exceptions import PasswordPolicyError
from src.application.register import RegisterCommand

from src.presentation.dependencies import RegisterServiceDepend


router = APIRouter(tags=['authorization'])


class RegisterIn(BaseModel):
    email: EmailStr
    password: SecretStr


class RegisterOut(BaseModel):
    detail: str


@router.post('/register')
@inject
async def register(body: RegisterIn, service: RegisterServiceDepend) -> RegisterOut:
    cmd = RegisterCommand(
        email=Email(body.email),
        password=Password(body.password.get_secret_value()),
    )

    try:
        await service.register(cmd)
    except PasswordPolicyError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        ) from e

    return RegisterOut(detail='Account created successfully! You can login now.')

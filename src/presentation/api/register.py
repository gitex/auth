from typing import Annotated

from dependency_injector.wiring import inject
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, EmailStr, SecretStr

from src.domain.value_objects import Email, Password

from src.application import RegisterCommand
from src.application.exceptions import PasswordPolicyError

from src.presentation.dependencies import RegisterServiceDepend
from src.presentation.validators import StrNotEmptyValidator


router = APIRouter(tags=['authorization'])


class RegisterIn(BaseModel):
    """Registration input.

    Do not put policies and business logic here, it's domain responsibility.
    """

    email: Annotated[EmailStr, StrNotEmptyValidator]
    password: Annotated[SecretStr, StrNotEmptyValidator]


class RegisterOut(BaseModel):
    detail: str
    user_id: str


@router.post('/register')
@inject
async def register(body: RegisterIn, service: RegisterServiceDepend) -> RegisterOut:
    cmd = RegisterCommand(
        email=Email(body.email),
        password=Password(body.password.get_secret_value()),
    )

    try:
        result = await service.register(cmd)
    except PasswordPolicyError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        ) from e

    return RegisterOut(
        detail='Account created successfully! You can login now.',
        user_id=str(result.account.identifier),
    )

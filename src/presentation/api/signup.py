from fastapi import APIRouter
from pydantic import BaseModel, EmailStr, SecretStr


router = APIRouter()


class SignupIn(BaseModel):
    email: EmailStr
    password: SecretStr


class SignupOut(BaseModel): ...


@router.post("/signup", response_model=SignupOut)
async def signup(body: SignupIn):
    return SignupOut()

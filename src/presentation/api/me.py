from uuid import UUID, uuid4

from fastapi import APIRouter
from pydantic import BaseModel


router = APIRouter(tags=['authorization'])


class MeOut(BaseModel):
    id: UUID
    email: str
    is_active: bool


@router.get('/me')
async def handler() -> MeOut:
    return MeOut(id=uuid4(), email='a@b.c', is_active=True)

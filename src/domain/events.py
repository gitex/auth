import typing as tp
from datetime import UTC, datetime

from pydantic import BaseModel, Field

from src.domain.value_objects import Email


class DomainEvent(BaseModel):
    occurred_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    def as_dict(self) -> dict[str, tp.Any]:
        return self.model_dump()


class UserRegistered(DomainEvent):
    user_id: str
    email: Email


class UserAuthorized(DomainEvent):
    user_id: str
    email: Email

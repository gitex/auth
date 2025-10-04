from datetime import datetime
from typing import final, override
from uuid import UUID

from sqlalchemy import TIMESTAMP, Index, String, func
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from .base import Base


@final
class Account(Base):
    __tablename__ = "accounts"
    __table_args__ = (Index("ix_account_email", "email"),)

    id: Mapped[UUID] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(30), unique=True)
    email: Mapped[str] = mapped_column(String(320), unique=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    is_email_verified: Mapped[bool] = mapped_column(default=False)
    is_active: Mapped[bool] = mapped_column(default=True, index=True)
    is_superuser: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), default=func.now(), nullable=False, onupdate=func.now()
    )

    @override
    def __repr__(self) -> str:
        return f"Account(id={self.id}, email={self.email})"

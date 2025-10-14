from datetime import datetime
from enum import StrEnum
from typing import Any, override

from sqlalchemy import Enum, Index, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from src.infra.dto import OutboxDto
from src.infra.orm.models.base import Base


class OutboxStatus(StrEnum):
    NEW = 'new'
    PUBLISHING = 'publishing'
    PUBLISHED = 'published'
    FAILED = 'failed'
    DLQ = 'dql'


# This affects index, change it carefully
READY_FOR_PUBLISH_STATUSES = [OutboxStatus.NEW, OutboxStatus.FAILED]


class Outbox(Base):
    __tablename__: str = 'outbox'

    id: Mapped[int] = mapped_column(primary_key=True)
    topic: Mapped[str] = mapped_column(String(80))
    key: Mapped[str | None] = mapped_column(String(120), default=None)
    payload: Mapped[dict[str, Any]] = mapped_column(JSONB, default=dict)
    headers: Mapped[dict[str, Any] | None] = mapped_column(JSONB, default=None)
    status: Mapped[OutboxStatus] = mapped_column(
        Enum(OutboxStatus), default=OutboxStatus.NEW
    )
    attempts: Mapped[int] = mapped_column(default=0)
    next_retry_at: Mapped[datetime | None] = mapped_column(default=None)
    error: Mapped[str | None] = mapped_column(String(256), default=None)
    published_at: Mapped[datetime | None] = mapped_column(default=None)
    kafka_partition: Mapped[int | None] = mapped_column(default=None)
    kafka_offset: Mapped[int | None] = mapped_column(default=None)

    __table_args__: tuple[Index] = (
        Index(
            'ix_partial_next_retry_at',
            'next_retry_at',
            postgresql_where=(status.in_(READY_FOR_PUBLISH_STATUSES)),
            postgresql_using='btree',
        ),
    )

    @override
    def __repr__(self) -> str:
        return f'Outbox #{self.id}, status={self.status.value}'

    @classmethod
    def from_dto(cls, outbox_dto: OutboxDto) -> 'Outbox':
        return cls(
            id=outbox_dto.id,
            topic=outbox_dto.topic,
            payload=outbox_dto.payload,
            headers=outbox_dto.headers,
        )

    def to_dto(self) -> OutboxDto:
        return OutboxDto(
            id=self.id,
            topic=self.topic,
            payload=self.payload,
            headers=self.headers or {},
        )

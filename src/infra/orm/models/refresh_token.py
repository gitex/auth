from datetime import datetime
from typing import Any, override
from uuid import UUID, uuid4

import sqlalchemy as sa
import sqlalchemy.dialects.postgresql as pg
from sqlalchemy.ext.mutable import MutableDict
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.domain.entities import Account

from src.infra.orm.models.base import Base, TimestampMixin


class RefreshFamily(TimestampMixin, Base):
    __tablename__: str = 'refresh_families'

    fid: Mapped[UUID] = mapped_column(
        pg.UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )
    fingerprint_hash: Mapped[str] = mapped_column(sa.String(256))
    version: Mapped[int] = mapped_column(default=0, nullable=False)
    expires_at: Mapped[datetime] = mapped_column(sa.TIMESTAMP(timezone=True), index=True)
    revoked_at: Mapped[datetime] = mapped_column(sa.TIMESTAMP(timezone=True))

    # прямые связи
    account_id: Mapped[UUID] = mapped_column(
        pg.UUID(as_uuid=True),
        sa.ForeignKey('accounts.id', ondelete='CASCADE'),
        nullable=False,
        index=True,
    )
    account: Mapped[UUID] = relationship('Account', back_populates='refresh_tokens')

    # обратные связи
    refresh_tokens: Mapped[list['RefreshToken']] = relationship(
        back_populates='family',
        cascade='all, delete-orphan',
        passive_deletes=True,
    )

    @override
    def __repr__(self) -> str:
        return f'RefreshFamily(fid={self.fid})'


class RefreshToken(TimestampMixin, Base):
    __tablename__: str = 'refresh_tokens'

    jti: Mapped[UUID] = mapped_column(
        pg.UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )
    hash: Mapped[str] = mapped_column(sa.String(256), unique=True)
    rotated_at: Mapped[datetime] = mapped_column(sa.TIMESTAMP(timezone=True))
    revoked_at: Mapped[datetime] = mapped_column(sa.TIMESTAMP(timezone=True))
    expires_at: Mapped[datetime] = mapped_column(sa.TIMESTAMP(timezone=True))
    last_used_at: Mapped[datetime] = mapped_column(sa.TIMESTAMP(timezone=True))
    meta: Mapped[dict[str, Any]] = mapped_column(
        MutableDict.as_mutable(pg.JSONB(astext_type=sa.Text())),
        server_default=sa.text("'{}'::jsonb"),
        default=dict,
    )

    # связи
    fid: Mapped[UUID] = mapped_column(
        pg.UUID(as_uuid=True),
        sa.ForeignKey('refresh_families.fid', ondelete='CASCADE'),
        index=True,
    )
    family: Mapped['RefreshFamily'] = relationship(
        back_populates='refresh_tokens',
    )

    account_id: Mapped[UUID] = mapped_column(
        pg.UUID(as_uuid=True),
        sa.ForeignKey('accounts.id', ondelete='CASCADE'),
        index=True,
    )
    account: Mapped['Account'] = relationship(
        back_populates='refresh_tokens',
    )

    rotation_parent_jti: Mapped[UUID | None] = mapped_column(
        pg.UUID(as_uuid=True),
        sa.ForeignKey('refresh_tokens.jti', ondelete='SET NULL'),
        index=True,
    )
    rotation_parent: Mapped['RefreshToken | None'] = relationship(
        back_populates='children',
    )

    @override
    def __repr__(self) -> str:
        return f'RefreshToken(jti={self.jti})'

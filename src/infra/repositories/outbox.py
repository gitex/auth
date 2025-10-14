from collections.abc import Sequence
from typing import Protocol, final

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.infra.dto import OutboxDto
from src.infra.orm.models import Outbox as OutboxDb
from src.infra.orm.models.outbox import READY_FOR_PUBLISH_STATUSES


class OutboxRepository(Protocol):
    async def create(self, outbox_dto: OutboxDto) -> None: ...
    async def ready_for_publishing(
        self, limit: int | None = None
    ) -> Sequence[OutboxDto]: ...


@final
class OutboxRepositoryDb:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, outbox_dto: OutboxDto) -> None:
        outbox_db = OutboxDb.from_dto(outbox_dto)
        self._session.add(outbox_db)

    async def ready_for_publishing(self, limit: int | None = None) -> Sequence[OutboxDto]:
        stmt = select(OutboxDb).where(OutboxDb.status.in_(READY_FOR_PUBLISH_STATUSES))
        if limit:
            stmt = stmt.limit(limit)
        result: Sequence[OutboxDb] = (await self._session.execute(stmt)).scalars().all()

        return [outbox_db.to_dto() for outbox_db in result]

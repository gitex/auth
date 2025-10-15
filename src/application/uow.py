from types import TracebackType
from typing import Protocol, Self, final, override

from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.ports import AccountRepository

from src.infra.orm.session import SessionFactory
from src.infra.repositories.account.db import DbAccountRepositoryImpl


class UnitOfWork(Protocol):
    accounts: AccountRepository

    async def __aenter__(self) -> Self: ...
    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None: ...
    async def commit(self) -> None: ...
    async def rollback(self) -> None: ...


@final
class SqlAlchemyUoW(UnitOfWork):
    def __init__(self, session_factory: SessionFactory) -> None:
        self._session_factory = session_factory
        self._session: AsyncSession | None = None

    @override
    async def __aenter__(self) -> Self:
        self._session: AsyncSession = self._session_factory()
        self.accounts: AccountRepository = DbAccountRepositoryImpl(self._session)
        return self

    @override
    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        if not self._session.begin():
            return

        try:
            if exc_type:
                await self.rollback()
            else:
                await self.commit()

        finally:
            await self._session.close()

    @override
    async def commit(self) -> None:
        await self._session.commit()

    @override
    async def rollback(self) -> None:
        await self._session.rollback()

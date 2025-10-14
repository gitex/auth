from types import TracebackType
from typing import Protocol, Self, override

from sqlalchemy.ext.asyncio import AsyncSession, AsyncSessionTransaction

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


class SqlAlchemyUoW(UnitOfWork):
    def __init__(self, session_factory: SessionFactory) -> None:
        self._session_factory = session_factory

    @override
    async def __aenter__(self) -> Self:
        self._session: AsyncSession = self._session_factory()

        self._transaction: AsyncSessionTransaction = self._session.begin()
        await self._transaction.__aenter__()
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
            await self._transaction.__aexit__(exc_type, exc, tb)

        finally:
            await self._session.close()

    @override
    async def commit(self) -> None:
        await self._session.commit()

    @override
    async def rollback(self) -> None:
        await self._session.rollback()

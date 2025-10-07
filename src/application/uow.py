from dataclasses import dataclass
from types import TracebackType
from typing import Protocol, Self

from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.ports import AccountRepository

from src.infra.orm.session import SessionFactory
from src.infra.repositories.account.db import DbAccountRepositoryImpl


class UnitOfWork(Protocol):
    session: AsyncSession  # TODO: Грязновато, реализация пролезла в протокол
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


@dataclass
class SqlAlchemyUoW(UnitOfWork):
    session_factory: SessionFactory

    async def __aenter__(self) -> Self:
        self.session = self.session_factory()
        self.accounts = DbAccountRepositoryImpl(self.session)
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        if not self.session:
            return

        try:
            if exc_type:
                await self.rollback()
            else:
                await self.commit()

        finally:
            await self.session.close()

    async def commit(self) -> None:
        await self.session.commit()

    async def rollback(self) -> None:
        await self.session.rollback()

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.entities import Account
from src.domain.ports import AccountRepository
from src.domain.value_objects import Email

from src.infra.mappers import account_db_to_account, account_to_account_db
from src.infra.orm.models import Account as AccountModel


class DbAccountRepositoryImpl(AccountRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_email(self, email: Email) -> Account | None:
        stmt = select(AccountModel).where(AccountModel.email == email.value)
        account_db: AccountModel | None = (
            await self.session.execute(stmt)
        ).scalar_one_or_none()

        if not account_db:
            return None

        return account_db_to_account(account_db)

    async def get_by_id(self, account_id: UUID) -> Account | None:
        account_db = await self.session.get(AccountModel, account_id)

        if not account_db:
            return None

        return account_db_to_account(account_db)

    async def create(self, account: Account) -> Account:
        account_db = account_to_account_db(account)
        self.session.add(account_db)
        await self.session.commit()
        await self.session.refresh(account_db)
        return account_db_to_account(account_db)

import logging
from typing import final, override
from uuid import UUID

from sqlalchemy import exists, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.entities import Account
from src.domain.ports import AccountRepository
from src.domain.specifications import Specification
from src.domain.value_objects import Email

from src.infra.mappers import account_db_to_account, account_to_account_db
from src.infra.orm.models import Account as AccountModel


logger = logging.getLogger(__name__)


@final
class DbAccountRepositoryImpl(AccountRepository):
    """Database implementation of AccountRepository using SQLAlchemy.

    This implementation provides persistence for Account aggregate roots
    using PostgreSQL database through SQLAlchemy async ORM.
    """

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    @override
    async def get_by_email(self, email: Email) -> Account | None:
        """Retrieve account by email address.

        Args:
            email: Email address to search for

        Returns:
            Account if found, None otherwise
        """
        logger.debug('Fetching account by email: %s', email.value)
        stmt = select(AccountModel).where(AccountModel.email == email.value)
        account_db: AccountModel | None = (
            await self.session.execute(stmt)
        ).scalar_one_or_none()

        if not account_db:
            logger.debug('Account not found for email: %s', email.value)
            return None

        logger.debug('Account found for email: %s', email.value)
        return account_db_to_account(account_db)

    @override
    async def get_by_id(self, account_id: UUID) -> Account | None:
        """Retrieve account by unique identifier.

        Args:
            account_id: UUID of the account

        Returns:
            Account if found, None otherwise
        """
        logger.debug('Fetching account by id: %s', account_id)
        account_db = await self.session.get(AccountModel, account_id)

        if not account_db:
            logger.debug('Account not found for id: %s', account_id)
            return None

        logger.debug('Account found for id: %s', account_id)
        return account_db_to_account(account_db)

    @override
    async def create(self, account: Account) -> Account:
        """Create a new account.

        Args:
            account: Account to create

        Returns:
            Created account with assigned identifier
        """
        logger.info('Creating new account for email: %s', account.email.value)
        account_db = account_to_account_db(account)
        self.session.add(account_db)
        await self.session.commit()
        await self.session.refresh(account_db)
        logger.info('Account created with id: %s', account_db.id)
        return account_db_to_account(account_db)

    async def exists(self, email: Email) -> bool:
        """Check if account with given email exists.

        Args:
            email: Email address to check

        Returns:
            True if account exists, False otherwise
        """
        logger.debug('Checking if account exists for email: %s', email.value)
        stmt = select(exists().where(AccountModel.email == email.value)).select_from(
            AccountModel
        )
        result = await self.session.execute(stmt)
        exists_result = result.scalar()
        logger.debug('Account exists for %s: %s', email.value, exists_result)
        return bool(exists_result)

    async def find_by_specification(self, spec: Specification[Account]) -> list[Account]:
        """Find accounts matching a specification.

        This method fetches all accounts and filters them in memory using
        the specification. For better performance with large datasets,
        consider implementing specification-to-SQL translation.

        Args:
            spec: Specification to match accounts against

        Returns:
            List of accounts satisfying the specification
        """
        logger.debug('Finding accounts by specification: %s', type(spec).__name__)
        stmt = select(AccountModel)
        result = await self.session.execute(stmt)
        accounts_db = result.scalars().all()

        accounts = [account_db_to_account(acc_db) for acc_db in accounts_db]
        filtered = [acc for acc in accounts if spec.is_satisfied_by(acc)]
        logger.debug(
            'Found %d accounts matching specification out of %d total',
            len(filtered),
            len(accounts),
        )
        return filtered

from src.domain.entities import Account
from src.domain.value_objects import Email, PasswordHash
from src.infra.orm.models import Account as AccountDb


def account_db_to_account(account_db: AccountDb) -> Account:
    return Account(
        identifier=account_db.id,
        email=Email(account_db.email),
        password_hash=PasswordHash(account_db.password_hash),
        is_active=account_db.is_active,
        roles=[],  # TODO: Добавить имплементацию ролей, когда будет готово
    )

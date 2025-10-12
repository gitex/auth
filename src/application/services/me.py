from dataclasses import dataclass

from src.domain.entities import Account
from src.domain.value_objects.account import AccessToken


@dataclass
class AccountService:
    def get_account(self, token: AccessToken) -> Account: ...

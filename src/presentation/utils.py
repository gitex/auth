import typing as tp

from fastapi import Depends

from src.domain.entities import Account


def get_current_user(token: tp.Annotated[str, Depends()]) -> Account: ...

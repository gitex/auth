import typing as tp

from pydantic import AfterValidator


def is_not_empty(value: str) -> str:
    if not value:
        raise ValueError('Is empty')
    return value


StrNotEmptyValidator = tp.Annotated[str, AfterValidator(is_not_empty)]

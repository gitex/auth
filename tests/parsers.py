from __future__ import annotations

from dataclasses import dataclass, fields
from http import HTTPStatus
from typing import Any

from httpx import Response


@dataclass(frozen=True)
class Error:
    loc: list[str]
    msg: str
    type: str

    @classmethod
    def from_dict(cls, kwargs: dict[str, Any]) -> Error:
        class_fields = {f.name for f in fields(cls)}
        return cls(**{k: v for k, v in kwargs.items() if k in class_fields})


@dataclass(frozen=True)
class Detail:
    errors: list[Error] | None = None

    def has_errors(self) -> bool:
        return bool(self.errors)

    def first_error(self) -> Error:
        if self.errors:
            return self.errors[0]

        raise ValueError('Response does not have errors')

    def has_error_for_field(self, field: str) -> bool:
        if not self.errors:
            return False

        return any(field in error.loc for error in self.errors)


def parse_unprocessable_entity_response(r: Response) -> Detail:
    errors: list[Error] = []

    if r.status_code != HTTPStatus.UNPROCESSABLE_ENTITY.value:
        raise TypeError(
            f'Response does not contain UNPROCESSABLE_ENTITY: {r.status_code}'
        )

    raw_detail = r.json().get('detail', None)
    if not raw_detail:
        raise ValueError(f'Cannot find "detail" in response: {r.json()}')

    errors = [Error.from_dict(error) for error in raw_detail]
    return Detail(errors)

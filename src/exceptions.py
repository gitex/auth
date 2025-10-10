from typing import Any


type ErrorCtx = dict[str, Any]


class BaseMicroserviceError(Exception):
    message: str = NotImplemented
    code: str = NotImplemented
    ctx: ErrorCtx | None = None

    def __init__(self, message: str | None = None, *, ctx: ErrorCtx) -> None:
        self.message = message or self.message
        self.ctx = ctx
        super().__init__(f'{self.message} ctx={ctx or {}}')

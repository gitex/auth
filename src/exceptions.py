from typing import Any


type ErrorCtx = dict[str, Any]


class MicroserviceError(Exception):
    message: str = NotImplemented
    code: str = NotImplemented
    ctx: ErrorCtx | None = None

    def __init__(self, ctx: ErrorCtx) -> None:
        self.ctx = ctx
        super().__init__(f"{self.message} ctx={ctx or {}}")

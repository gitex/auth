from __future__ import annotations

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from src.application.exceptions import InvalidCredentialsError


async def invalid_credentials(_: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={'detail': 'Invalid email or password'},
    )


def add_custom_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(InvalidCredentialsError, invalid_credentials)

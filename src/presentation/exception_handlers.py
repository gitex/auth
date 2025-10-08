from fastapi import Request, status
from fastapi.responses import JSONResponse

from src.domain.exceptions import InvalidCredentialsError

from .main import app


@app.exception_handler(InvalidCredentialsError)
async def invalid_credentials(  # noqa: RUF029
    _: Request,
    exc: InvalidCredentialsError,
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={'detail': 'Invalid email or password'},
    )

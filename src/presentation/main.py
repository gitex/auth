from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.infra.config import settings

from src.bootstrap.wiring import AuthContainer

from src.presentation import api as api_package
from src.presentation.exception_handlers import add_custom_exception_handlers

from .api.login import router as login_router
from .api.register import router as register_router


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None]:  # noqa: RUF029
    yield


container = AuthContainer()
container.config.from_pydantic(settings)
container.wire(packages=[api_package])


def create_app() -> FastAPI:
    app = FastAPI(
        debug=settings.debug,
        title=settings.app_name,
        lifespan=lifespan,
    )

    app.include_router(login_router)
    app.include_router(register_router)

    add_custom_exception_handlers(app)

    return app


app = create_app()

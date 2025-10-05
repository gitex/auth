from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.infra.config import settings

from .api.login import router as auth_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(
    debug=settings.debug,
    title=settings.app_name,
    lifespan=lifespan,
)

app.include_router(auth_router)

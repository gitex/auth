from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.config import settings

from .api.router import router as auth_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(
    debug=settings.debug,
    title=settings.app_name,
    lifespan=lifespan,
)

app.include_router(auth_router)

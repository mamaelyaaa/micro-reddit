from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import ORJSONResponse
from sqlalchemy import text

from api import router as main_router
from core import settings, db_helper
from core.dependencies import SessionDep
from core.exceptions import AppException
from schemas import BaseResponseSchema


@asynccontextmanager
async def lifespan(_: FastAPI):
    # Startup
    yield
    # Shutdown
    await db_helper.dispose()


app = FastAPI(
    title=settings.api.title,
    version=settings.api.version,
    lifespan=lifespan,
    default_response_class=ORJSONResponse,
)

app.include_router(main_router)


@app.get("/", response_model=BaseResponseSchema)
def get_root():
    return BaseResponseSchema(detail="Api is working!")


@app.get("/health-check", response_model=BaseResponseSchema)
async def get_db_connection(session: SessionDep):
    pg_version = await session.scalar(text("SELECT VERSION()"))
    return BaseResponseSchema(detail=str(pg_version))


@app.exception_handler(AppException)
async def handle_app_exception(request: Request, exc: AppException):
    return ORJSONResponse(status_code=exc.status_code, content={"detail": exc.message})


if __name__ == "__main__":
    uvicorn.run(
        app="src.main:app",
        reload=True,
        host=settings.run.host,
        port=settings.run.port,
    )

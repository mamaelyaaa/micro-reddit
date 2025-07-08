import logging

import uvicorn
from fastapi import FastAPI
from sqlalchemy import text

from core import settings
from core.dependencies import SessionDep
from core.logger import setup_logging
from schemas import BaseResponseSchema

setup_logging()
logger = logging.getLogger(__name__)


app = FastAPI(
    title=settings.api.title,
    version=settings.api.version,
)


@app.get("/", response_model=BaseResponseSchema)
def get_root():
    return BaseResponseSchema(detail="Api is working!")


@app.get("/health-check", response_model=BaseResponseSchema)
async def get_db_connection(session: SessionDep):
    pg_version = await session.scalar(text("SELECT VERSION()"))
    return BaseResponseSchema(detail=str(pg_version))


if __name__ == "__main__":
    uvicorn.run(
        app="src.main:app",
        reload=True,
        host=settings.run.host,
        port=settings.run.port,
    )

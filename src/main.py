import uvicorn
from fastapi import FastAPI
from sqlalchemy import text

from core import settings
from core.dependencies import SessionDep

app = FastAPI(
    title=settings.api.title,
    version=settings.api.version,
)


@app.get("/")
def get_root():
    return {"message": "Api is working!"}


@app.get("/health-check")
async def get_db_connection(session: SessionDep):
    pg_version = await session.scalar(text("SELECT VERSION()"))
    return {"message": str(pg_version)}


if __name__ == "__main__":
    uvicorn.run(
        app="src.main:app",
        reload=True,
        host=settings.run.host,
        port=settings.run.port,
    )

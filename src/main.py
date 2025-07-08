import uvicorn
from fastapi import FastAPI

from core.config import settings

app = FastAPI(
    title=settings.api.title,
    version=settings.api.version,
)


@app.get("/")
def get_root():
    return {"message": "Api is working!"}


if __name__ == "__main__":
    uvicorn.run(
        app="src.main:app",
        reload=True,
        host=settings.run.host,
        port=settings.run.port,
    )

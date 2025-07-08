from pathlib import Path
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel


class RunConfig(BaseModel):
    mode: Literal["DEV", "TEST", "PROD"] = "DEV"
    host: str = "127.0.0.1"
    port: int = 8000


class ApiConfig(BaseModel):
    title: str = "c-reddit-backend"
    version: str = "0.0.0"


class FilesConfig(BaseModel):
    # Базовые пути
    base_dir: Path = Path(__file__).resolve().parent.parent.parent
    src_dir: Path = base_dir / "src"


class Settings(BaseSettings):
    api: ApiConfig = ApiConfig()
    run: RunConfig = RunConfig()
    files: FilesConfig = FilesConfig()

    model_config = SettingsConfigDict()


settings = Settings()

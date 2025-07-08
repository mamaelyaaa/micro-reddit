from pathlib import Path
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel, PostgresDsn


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

    # Переменные окружения
    env_file: Path = base_dir / ".env"
    env_example_file: Path = base_dir / ".env.example"


class DatabaseConfig(BaseModel):
    username: str
    password: str
    host: str
    port: int
    name: str

    echo: int = 0

    @property
    def POSTGRES_DSN(self):
        return f"postgresql+asyncpg://{self.username}:{self.password}@{self.host}:{self.port}/{self.name}"


# class BrokerConfig(BaseModel):
#
#     @property
#     def AMQP_DSN(self):
#         return f"amqp://{self.username}:{self.password}@{self.host}:{self.port}//"


class Settings(BaseSettings):
    api: ApiConfig = ApiConfig()
    run: RunConfig = RunConfig()
    files: FilesConfig = FilesConfig()

    db: DatabaseConfig

    model_config = SettingsConfigDict(
        env_file=(files.env_example_file, files.env_file),
        case_sensitive=False,
        env_nested_delimiter="__",
        env_file_encoding="utf-8",
    )


settings = Settings()

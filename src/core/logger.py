import logging
import logging.handlers
import sys
from typing import Literal

from .config import settings


def setup_logging() -> None:
    settings.files.logs_dir.mkdir(exist_ok=True)

    root_logger = logging.getLogger()
    root_logger.setLevel(settings.log.level)

    formatter = logging.Formatter(settings.log.format)

    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)

    file_handler = logging.FileHandler(settings.files.logs_file, encoding="utf-8")
    file_handler.setFormatter(formatter)

    if root_logger.hasHandlers():
        root_logger.handlers.clear()

    root_logger.addHandler(stream_handler)
    root_logger.addHandler(file_handler)

    logging.getLogger("asyncio").setLevel(logging.WARNING)
    logging.getLogger("aio_pika").setLevel(logging.INFO)
    logging.getLogger("aiormq").setLevel(logging.INFO)


class MicroRedditLogger:

    def __init__(self, log_level: Literal["DEBUG", "INFO"], log_format: str):
        self.log_level = log_level
        self.log_format = log_format
        self._logger_startup()

    @staticmethod
    def _logger_startup():
        settings.files.logs_dir.mkdir(exist_ok=True)

        root_logger = logging.getLogger()
        root_logger.setLevel(settings.log.level)

        formatter = logging.Formatter(settings.log.format)

        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setFormatter(formatter)

        file_handler = logging.FileHandler(settings.files.logs_file, encoding="utf-8")
        file_handler.setFormatter(formatter)

        if root_logger.hasHandlers():
            root_logger.handlers.clear()

        root_logger.addHandler(stream_handler)
        root_logger.addHandler(file_handler)


app_logger = MicroRedditLogger(
    log_level=settings.log.level, log_format=settings.log.format
)

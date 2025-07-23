import logging
import logging.handlers
import sys

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

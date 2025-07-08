import logging
import logging.handlers
import sys

from .config import settings


def setup_logging() -> None:
    settings.files.logs_dir.mkdir(exist_ok=True)

    logging.basicConfig(
        level=settings.log.level,
        format=settings.log.format,
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler(settings.files.logs_file, encoding="utf-8"),
        ],
    )

import logging
import os
import sys

from loguru import logger


def configure_logger():
    logger.remove()
    log_format = "{time:YYYY-MM-DD HH:mm:ss.SSS} [{level}] {name}:{line} — <level>{message}</level>"
    logger.configure()
    logger.add(
        sys.stdout,
        level=os.environ.get("LOGURU_LEVEL", "INFO"),
        format=log_format,
        serialize=False,
        filter=lambda record: record["level"].no <= logging.INFO,
        enqueue=True,
    )
    logger.add(
        sys.stderr,
        level="INFO",
        format=log_format,
        serialize=False,
        filter=lambda record: record["level"].no > logging.INFO,
        enqueue=True,
    )

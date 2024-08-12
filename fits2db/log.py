"""
Logging configuration module for Fits2db.

This module sets up and configures logging for the Fits2db package, supporting
various log levels and formats. Logs can be directed to both the console and an
optional debug file.

!!! note "Example usage"
    ```python title="entry point of programm"
    from .log import configure_logger

    level = "DEBUG"
    log = configure_logger(level)
    log.info("Some Message")
    ```
    ```python title="Usage in other modules"
    level = "DEBUG"
    configure_logger(level)
    ```
"""

from __future__ import annotations

import logging
import sys


LOG_LEVELS = {
    "ERROR": logging.ERROR,
    "WARNING": logging.WARNING,
    "INFO": logging.INFO,
    "DEBUG": logging.DEBUG,
}

LOG_FORMATS = {
    "ERROR": "%(levelname)-8s - %(asctime)s - %(pathname)s - %(funcName)s: %(message)s",
    "WARNING": "%(levelname)-8s - %(asctime)s: %(message)s",
    "INFO": "%(levelname)-8s - %(asctime)s: %(message)s",
    "DEBUG": "%(levelname)-8s - %(asctime)s - %(pathname)s - %(funcName)s: %(message)s",
}

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def configure_logger(
    level: str = "DEBUG", debug_file: str | None = None
) -> logging.Logger:
    """Configure logging for python_package.

    Set up logging to stdout with given level. If ``debug_file`` is given set
    up logging to file with DEBUG level.
    """
    logger = logging.getLogger("fits2db")
    logger.setLevel(logging.DEBUG)

    # Remove all attached handlers, in case there was
    # a logger with using the name 'fits2db'
    del logger.handlers[:]

    # Create a file handler if a log file is provided
    if debug_file is not None:
        debug_formatter = logging.Formatter(
            LOG_FORMATS["DEBUG"], datefmt=DATE_FORMAT
        )
        file_handler = logging.FileHandler(debug_file)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(debug_formatter)
        logger.addHandler(file_handler)

    log_level = LOG_LEVELS.get(level, logging.DEBUG)
    log_formatter = logging.Formatter(
        LOG_FORMATS.get(level, LOG_FORMATS["DEBUG"]), datefmt=DATE_FORMAT
    )

    # Create a stream handler
    stream_handler = logging.StreamHandler(stream=sys.stdout)
    stream_handler.setLevel(log_level)
    stream_handler.setFormatter(log_formatter)
    logger.addHandler(stream_handler)

    return logger

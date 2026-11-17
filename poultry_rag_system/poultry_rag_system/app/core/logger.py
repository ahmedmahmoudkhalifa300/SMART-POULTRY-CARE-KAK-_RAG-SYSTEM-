"""
Shared application logger.

Usage:
    from app.core.logger import get_logger
    logger = get_logger(__name__)
    logger.info("Something happened")
"""

import logging
import sys

_CONFIGURED = False


def _configure_root_logger(level: int = logging.INFO) -> None:
    global _CONFIGURED
    if _CONFIGURED:
        return

    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    handler.setFormatter(formatter)

    root = logging.getLogger()
    root.setLevel(level)
    root.addHandler(handler)
    _CONFIGURED = True


def get_logger(name: str) -> logging.Logger:
    """Return a module-scoped logger with consistent formatting."""
    _configure_root_logger()
    return logging.getLogger(name)


# TODO: consider swapping this for `loguru` (already in requirements.txt)
# if we want structured/JSON logs or automatic log rotation later.

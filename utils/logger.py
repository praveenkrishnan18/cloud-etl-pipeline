"""
utils/logger.py — Centralized logging setup
All pipeline modules import from here so log format is consistent.
"""

import logging
import sys


def get_logger(name: str) -> logging.Logger:
    """
    Returns a logger that:
      - Writes to stdout (GitHub Actions captures this automatically)
      - Uses a clean, timestamped format
      - Is safe to call multiple times (won't add duplicate handlers)
    """
    logger = logging.getLogger(name)

    if not logger.handlers:                         # Prevent duplicate handlers
        logger.setLevel(logging.INFO)

        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.INFO)

        formatter = logging.Formatter(
            fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger

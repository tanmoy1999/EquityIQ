import logging
import sys
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path

# ---- Config ----
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

LOG_FILE = LOG_DIR / "app.log"
LOG_LEVEL = logging.DEBUG   # change to DEBUG if needed


def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)

    # Prevent duplicate handlers
    if logger.handlers:
        return logger

    logger.setLevel(LOG_LEVEL)

    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # 🔥 Date-based rotating file handler
    file_handler = TimedRotatingFileHandler(
        filename=LOG_DIR / "app.log",
        when="midnight",       # rotate daily
        interval=1,
        backupCount=30,        # keep last 30 days
        encoding="utf-8",
        utc=False              # set True if running on UTC servers
    )

    # Suffix controls filename format
    file_handler.suffix = "%Y-%m-%d"

    file_handler.setFormatter(formatter)
    file_handler.setLevel(LOG_LEVEL)

    logger.addHandler(file_handler)
    logger.propagate = False

    return logger
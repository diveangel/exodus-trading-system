"""Logging configuration for the application."""

import logging
import sys
from pathlib import Path
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime

from app.config import settings


def setup_logging():
    """
    Setup application logging with file rotation.

    - Logs are written to logs/app.log
    - Rotation: Daily at midnight
    - Retention: 2 days
    - Format: timestamp - level - module - message
    """
    # Create logs directory
    log_dir = Path(__file__).parent.parent.parent / "logs"
    log_dir.mkdir(exist_ok=True)

    # Log file path
    log_file = log_dir / "app.log"

    # Define log format
    log_format = "%(asctime)s - %(levelname)s - %(name)s - %(funcName)s:%(lineno)d - %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"

    # Create formatters
    formatter = logging.Formatter(log_format, datefmt=date_format)

    # Root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)

    # Remove existing handlers
    root_logger.handlers.clear()

    # Console handler (stdout)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)

    # File handler with daily rotation
    file_handler = TimedRotatingFileHandler(
        filename=str(log_file),
        when="midnight",  # Rotate at midnight
        interval=1,  # Every 1 day
        backupCount=2,  # Keep 2 days of logs
        encoding="utf-8",
        utc=False,  # Use local time
    )
    file_handler.setLevel(logging.DEBUG)  # Capture all levels to file
    file_handler.setFormatter(formatter)
    file_handler.suffix = "%Y-%m-%d"  # Add date suffix to rotated files
    root_logger.addHandler(file_handler)

    # Set specific loggers
    # SQLAlchemy - reduce noise
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)

    # Uvicorn - keep INFO level
    logging.getLogger("uvicorn").setLevel(logging.INFO)
    logging.getLogger("uvicorn.access").setLevel(logging.INFO)

    # Our application - DEBUG level
    logging.getLogger("app").setLevel(logging.DEBUG)

    # Log startup message
    root_logger.info("=" * 80)
    root_logger.info(f"Logging initialized - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    root_logger.info(f"Log file: {log_file}")
    root_logger.info(f"Log level: {root_logger.level}")
    root_logger.info(f"Debug mode: {settings.DEBUG}")
    root_logger.info("=" * 80)

    return root_logger


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance.

    Args:
        name: Logger name (usually __name__)

    Returns:
        Logger instance
    """
    return logging.getLogger(name)

# Logger utility
from loguru import logger
import sys
import os

def setup_logger():
    """Configure loguru logger with file and console handlers"""
    # Remove default handler
    logger.remove()

    # Create logs directory if it doesn't exist
    os.makedirs("reports/logs", exist_ok=True)

    # Add console handler only if stdout is available (not in windowed mode)
    if sys.stdout is not None:
        logger.add(
            sys.stdout,
            format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <level>{message}</level>",
            level="INFO"
        )

    # Add file handler
    logger.add(
        "reports/logs/automation_{time:YYYY-MM-DD}.log",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {message}",
        level="INFO",
        rotation="1 day",
        retention="7 days"
    )

    return logger
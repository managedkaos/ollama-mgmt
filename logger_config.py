"""
Shared logging configuration
"""

import logging
import os


def setup_logger(name):
    """
    Configure and return a logger with consistent settings.

    Args:
        name (str): Name of the logger (typically __name__ from the calling module)
        logs_path (str): Path to logs directory

    Returns:
        logging.Logger: Configured logger instance
    """
    logs_path = os.environ.get("LOGS_PATH", "./logs")

    # Create directories if they don't exist
    try:
        os.makedirs(logs_path, exist_ok=True)
    except OSError as e:
        print(f"Failed to create directory: {e}")
        raise

    # Create logger
    logger = logging.getLogger(name)

    # Configure logging format and handlers
    formatter = logging.Formatter("%(asctime)s - %(levelname)s: %(message)s")

    # File handler
    file_handler = logging.FileHandler(f"{logs_path}/{name}.log")
    file_handler.setFormatter(formatter)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # Add handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    # Set default level
    logger.setLevel(logging.INFO)

    # Check environment variable for custom log level
    env_logging_level = os.environ.get("LOGGING_LEVEL")
    if env_logging_level:
        try:
            level = getattr(logging, env_logging_level.upper())
            if level in [logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR]:
                logger.setLevel(level)
            else:
                print(
                    f"Invalid logging level: {env_logging_level}. Defaulting to INFO."
                )
        except AttributeError:
            print(f"Invalid logging level: {env_logging_level}. Defaulting to INFO.")

    return logger

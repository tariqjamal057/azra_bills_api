"""This module provides a custom logger configuration for the application."""

import logging
from typing import Union


def get_logger(
    name: str, level: int = logging.INFO, log_id: Union[str, id] = None
) -> logging.Logger:
    """Create and configure a logger with the specified parameters.

    Args:
        name (str): The name of the logger.
        level (int, optional): The logging level. Defaults to logging.INFO.
        log_id (Union[str, id], optional): An optional identifier for the logger. Defaults to None.

    Returns:
        logging.Logger: A configured logger instance.

    Example:
        >>> logger = get_logger("my_app", level=logging.DEBUG, log_id="123")
        >>> logger.info("This is an info message")
    """
    logger = logging.Logger(name)
    logger.setLevel(level)
    console = logging.StreamHandler()
    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
    console.setFormatter(formatter)
    logger.addHandler(console)

    if log_id:
        logger = logging.LoggerAdapter(logger, {"log_id", log_id})

    return logger


logger = get_logger(__name__)

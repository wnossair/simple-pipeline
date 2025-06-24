# logging_config.py
"""This module contains functions for setting up logging configuration."""

import logging
from logging.handlers import RotatingFileHandler

def setup_logging(log_file: str) -> logging.Logger:
    """Set up a logger with both file and console handlers.
    
    This function configures a logger to write logs to a specified file with 
    rotating capabilities, and also outputs logs to the console. It sets the logging level 
    to INFO and uses a formatter that includes the timestamp, log level, and message.

    Args:
        log_file (str): The path to the log file where logs will be written.
    
    Returns:
        logging.Logger: A configured logger instance.
    """

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    # Create formatters
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    # File handler with rotation
    file_handler = RotatingFileHandler(log_file, maxBytes=10_000_000, backupCount=5)
    file_handler.setFormatter(formatter)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # Add handlers to logger
    logger.handlers = []  # Clear existing handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger

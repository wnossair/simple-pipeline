# logging_config.py
import logging
from logging.handlers import RotatingFileHandler

def setup_logging(log_file: str) -> logging.Logger:
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
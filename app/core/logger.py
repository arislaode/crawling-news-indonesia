import logging
from logging.handlers import RotatingFileHandler
import os

def setup_logger(name):
    """Setup and return a logger with the specified name."""
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Create handlers
    c_handler = logging.StreamHandler()
    f_handler = RotatingFileHandler(
        os.path.join('logs', f'{name}.log'), maxBytes=1048576, backupCount=10
    )

    # Create formatters and add it to handlers
    c_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
    f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    c_handler.setFormatter(c_format)
    f_handler.setFormatter(f_format)

    # Add handlers to the logger
    logger.addHandler(c_handler)
    logger.addHandler(f_handler)

    return logger

# Ensure the logs directory exists
if not os.path.exists('logs'):
    os.makedirs('logs')

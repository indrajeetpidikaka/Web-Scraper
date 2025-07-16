import logging
import sys
from logging.handlers import RotatingFileHandler
import os

def setup_logger(level=logging.INFO):
    """
    Sets up the root logger.
    """
    # Create logs directory if not exists
    os.makedirs("logs", exist_ok=True)
    
    logger = logging.getLogger()
    logger.setLevel(level)
    
    # Clear existing handlers to prevent duplicate logs if called multiple times
    if logger.hasHandlers():
        logger.handlers.clear()
    
    # Formatting for log messages
    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)-8s] [%(module)s.%(funcName)s:%(lineno)d] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    
    # File handler: logs to a file, rotates when size limit is reached
    file_handler = RotatingFileHandler(
        "logs/scraper.log", 
        maxBytes=10*1024*1024, # 10 MB
        backupCount=3,         # Keep 3 old log files
        encoding='utf-8'       # Ensure proper character encoding
    )
    file_handler.setFormatter(formatter)
    
    # Console handler: logs to standard output (console)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    
    # Add both handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    # Suppress excessive logging from urllib3 (used by requests)
    http_logger = logging.getLogger("urllib3")
    http_logger.setLevel(logging.WARNING)
    
    logging.info("Logger initialized.")

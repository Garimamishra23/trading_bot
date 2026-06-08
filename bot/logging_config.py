import logging
import os
from datetime import datetime

def setup_logging(log_dir="logs"):
    os.makedirs(log_dir, exist_ok=True)
    
    log_file = os.path.join(log_dir, f"trading_bot_{datetime.now().strftime('%Y%m%d')}.log")
    
    logger = logging.getLogger("trading_bot")
    logger.setLevel(logging.DEBUG)
    
    if logger.handlers:
        return logger

    # File handler — captures everything (DEBUG+)
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    ))

    # Console handler — only important stuff (INFO+)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(message)s",
        datefmt="%H:%M:%S"
    ))

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    return logger

def get_logger(name):
    return logging.getLogger(f"trading_bot.{name}")
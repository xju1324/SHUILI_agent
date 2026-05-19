import os
import logging
from datetime import datetime

DEFAULT_LOG_FORMAT = "%(asctime)s | %(levelname)-7s | %(name)-30s | %(message)s"


def get_logger(
    name: str,
    console_level: int = logging.INFO,
    file_level: int = logging.DEBUG,
    log_dir: str = None,
) -> logging.Logger:
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger

    logger.setLevel(logging.DEBUG)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(console_level)
    console_handler.setFormatter(logging.Formatter(
        "\033[36m%(asctime)s\033[0m | \033[33m%(levelname)-7s\033[0m | \033[32m%(name)-30s\033[0m | %(message)s"
    ))
    logger.addHandler(console_handler)

    if log_dir is None:
        log_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "logs")
    os.makedirs(log_dir, exist_ok=True)
    today = datetime.now().strftime("%Y%m%d")
    log_file = os.path.join(log_dir, f"agent_{today}.log")

    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setLevel(file_level)
    file_handler.setFormatter(logging.Formatter(DEFAULT_LOG_FORMAT))
    logger.addHandler(file_handler)

    return logger

from datetime import date
import logging
from itsdangerous import URLSafeSerializer
from typing import Any

def get_logger(name: str, log_level: str = "WARNING"):
    logger = logging.getLogger(name)
    logger.setLevel(log_level)

    stream_handler = logging.StreamHandler()
    formatter = logging.Formatter(
        "{asctime} - {levelname} - {message}", style="{", datefmt="%Y-%m-%d %H:%M"
    )
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    return logger

def get_date():

    return date.today().strftime("%d %B %Y")
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

def sign_data(data: Any, secret_key: str|bytes, salt=str|bytes|None):
    s = URLSafeSerializer(secret_key, salt)
    signed_data = s.dumps(data)
    return signed_data

def load_signed_data(signed_data: str|bytes, secret_key: str|bytes, salt=str|bytes|None):
    s = URLSafeSerializer(secret_key, salt)
    data = s.loads(signed_data)
    return data
    

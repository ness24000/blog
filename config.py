import os

from werkzeug.security import generate_password_hash


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY") or "my_secret_key"
    LOG_LEVEL = os.getenv("LOG_LEVEL") or "DEBUG"
    PATH_TO_DB = os.getenv("PATH_TO_DB") or "./data/posts.db"
    ADMIN_KEY_HASH = generate_password_hash(os.getenv("ADMIN_KEY"))

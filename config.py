import os

from werkzeug.security import generate_password_hash


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY") or "my_secret_key"
    LOG_LEVEL = os.getenv("LOG_LEVEL") or "DEBUG"
    PATH_TO_DB = os.getenv("PATH_TO_DB") or "./data/posts.db"
    POOL_SIZE = int(os.getenv("POOL_SIZE"))
    MAX_POOL_OVERFLOW = int(os.getenv("MAX_POOL_OVERFLOW"))
    PATH_TO_MEDIA_FOLDER = os.path.abspath(os.getenv("PATH_TO_MEDIA_FOLDER") or "./data/media")
    ADMIN_KEY_HASH = generate_password_hash(os.getenv("ADMIN_KEY"))
    DOMAIN_NAME = os.getenv("DOMAIN_NAME") or "localhost:8080"

    MAIL_SERVER = os.getenv("MAIL_SERVER")
    MAIL_PORT = int(os.getenv("MAIL_PORT"))
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False

    CELERY = {
        "broker_url": os.getenv("CELERY_BROKER_URL"),
        "result_backend": os.getenv("CELERY_RESULT_BROKER"),
        "task_ignore_result": True,
    }

    LIMITER_STORAGE_URI = os.getenv("LIMITER_STORAGE_URI")

    MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 10 MB upload limit

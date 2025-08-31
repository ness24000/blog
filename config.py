import os

from werkzeug.security import generate_password_hash


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY") or "my_secret_key"
    LOG_LEVEL = os.getenv("LOG_LEVEL") or "DEBUG"
    PATH_TO_DB = os.getenv("PATH_TO_DB") or "./data/posts.db"
    ADMIN_KEY_HASH = generate_password_hash(os.getenv("ADMIN_KEY"))
    
    MAIL_SERVER = os.getenv("MAIL_SERVER")
    MAIL_PORT = int(os.getenv("MAIL_PORT"))
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAILTRAP_API_KEY")
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
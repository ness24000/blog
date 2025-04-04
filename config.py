import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    LOG_LEVEL = os.environ.get("LOG_LEVEL") or "WARNING"
    PATH_TO_DB = os.environ.get("PATH_TO_DB")

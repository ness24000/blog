import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    LOG_LEVEL = os.getenv("LOG_LEVEL") or "WARNING"
    PATH_TO_DB = os.getenv("PATH_TO_DB")

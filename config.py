import os


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY") or "my_secret_key"
    LOG_LEVEL = os.getenv("LOG_LEVEL") or "DEBUG"
    PATH_TO_DB = os.getenv("PATH_TO_DB") or "./posts.db"
    ADMIN_KEY_HASH = "scrypt:32768:8:1$fsh0zPgobLvU1C57$da6ee34835fc8fc1ffd0538c1ab9cd0062a7b4eb49980a54e1d593c453b3955f95c176ba124551aac2bc10e6410390589fa5e7a522dea0057f098bb3d53247fd"

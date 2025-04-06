import os


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY") or "my_secret_key"
    LOG_LEVEL = os.getenv("LOG_LEVEL") or "DEBUG"
    PATH_TO_DB = os.getenv("PATH_TO_DB") or "./posts.db"
    ADMIN_KEY_HASH = "scrypt:32768:8:1$jtIxkfcvMktwW3br$4280458f91fa3c0164f2d07eb9582f96e17e4a21de2f6c8f41d91ab06cea7d3a541281c15391f21517bed6b515f7fc97c9e26fccbd4add4a47c7ee18e25fd1b8"

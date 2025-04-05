import os


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY") or "my_secret_key"
    LOG_LEVEL = os.getenv("LOG_LEVEL") or "DEBUG"
    PATH_TO_DB = os.getenv("PATH_TO_DB") or "./posts.db"
    ADMIN_KEY_HASH = "scrypt:32768:8:1$vsYRbuYfRdj2SU5i27cf$a5b343c86e2ceaf1f9374ce1ecdcac9283bf5370da632285311207355a134f0ff0b1169977327f2b24ac27b4b565e970570e4401fdb6eb91ca14b98af2412b94"

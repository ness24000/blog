import os

from config import Config
from flask import Flask

from app.posts_management import connect_to_db, initialize_db
from app.utils import get_logger

app = Flask(__name__)
app.config.from_object(Config)

logger = get_logger(__name__, app.config["LOG_LEVEL"])


nitialize_db(app.config["PATH_TO_DB"])
cur = connect_to_db(app.config["PATH_TO_DB"])


from app import routes

logger.debug(f"Blog initialization finished")

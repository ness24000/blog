import os

from flask import Flask
from flask_mail import Mail
from werkzeug.middleware.proxy_fix import ProxyFix

from app.celery_init_app import celery_init_app
from app.db_interface import connect_to_db, initialize_db
from app.utils import get_logger
from config import Config

from app.DBHandler import DBHandler

app = Flask(__name__)
app.config.from_object(Config)

logger = get_logger(__name__, app.config["LOG_LEVEL"])

dbHandler = DBHandler(
    app.config["PATH_TO_DB"],
    logger,
    app.config["MAX_POOL_OVERFLOW"],
    app.config["POOL_SIZE"],
)

mail = Mail(app)
celery_app = celery_init_app(app)

# necessary if app behind reverse proxy
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1)


from app import errorhandlers, routes

logger.debug(f"Blog initialization finished")

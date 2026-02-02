import os

from flask import Flask

from werkzeug.middleware.proxy_fix import ProxyFix

from app.celery_init_app import celery_init_app
from app.utils import get_logger
from config import Config

from app.DBHandler import DBHandler
from app.PostsHandler import PostsHandler
from app.MailHandler import MailHandler

app = Flask(__name__)
app.config.from_object(Config)

# necessary if app behind reverse proxy
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1)

logger = get_logger(__name__, app.config["LOG_LEVEL"])

db_handler = DBHandler(
    app.config["PATH_TO_DB"],
    logger,
    app.config["MAX_POOL_OVERFLOW"],
    app.config["POOL_SIZE"],
)

posts_handler = PostsHandler(db_handler, logger)
mail_handler = MailHandler(app,db_handler,logger)

celery_app = celery_init_app(app)

from app import errorhandlers, routes

logger.debug(f"Blog initialization finished")

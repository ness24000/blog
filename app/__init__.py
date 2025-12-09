import os

from flask import Flask
from flask_mail import Mail
from werkzeug.middleware.proxy_fix import ProxyFix

from app.celery_init_app import celery_init_app
from app.db_interface import connect_to_db, initialize_db
from app.utils import get_logger
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

mail = Mail(app)    
celery_app = celery_init_app(app)

# necessary if app behind reverse proxy
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1)


logger = get_logger(__name__, app.config["LOG_LEVEL"])


initialize_db(app.config["PATH_TO_DB"])
cur = connect_to_db(app.config["PATH_TO_DB"])


from app import errorhandlers, routes

logger.debug(f"Blog initialization finished")

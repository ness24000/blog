from flask import Flask, redirect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

def limiter_init(app: Flask)->Limiter:
    limiter = Limiter(
        get_remote_address,
        app=app,
        default_limits=["200 per day", "50 per hour"],
        default_limits_per_method=True,
        storage_uri=app.config["LIMITER_STORAGE_URI"],
        storage_options={"socket_connect_timeout": 30},
    )
    return limiter
from flask import redirect
from app import app, logger

@app.errorhandler(429)
def ratelimit_handler(e):
    logger.warning(f"Rate limit reached: {e}")
    return redirect("https://en.wikipedia.org/wiki/Rate_limiting")
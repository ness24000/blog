#!/bin/sh
celery -A app.celery_app worker -D
gunicorn -b 0.0.0.0:8080 blog_app:app
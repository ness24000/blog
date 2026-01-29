#!/bin/sh
celery multi start w1 -A app:celery_app -l INFO
gunicorn -b 0.0.0.0:8080 blog_app:app
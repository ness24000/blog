#!/bin/sh

# start a celery worker in the background 
celery multi start w1 -A app:celery_app -l INFO

# start flask application via gunicorn, publicly (i.e. 0.0.0.0:...)
gunicorn -b 0.0.0.0:8080 blog_app:app
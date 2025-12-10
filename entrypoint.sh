#!/bin/sh
gunicorn -b 0.0.0.0:8080 blog_app:app
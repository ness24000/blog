FROM python:3.13.3
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY config.py .
COPY blog_app.py .
COPY entrypoint.sh .
RUN chmod +x entrypoint.sh
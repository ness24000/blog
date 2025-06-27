FROM nginx

RUN apt update
RUN apt install -y python3 python3-dev python3-venv libaugeas-dev gcc
RUN python3 -m venv /opt/certbot/ && /opt/certbot/bin/pip install --upgrade pip
RUN /opt/certbot/bin/pip install certbot certbot-nginx
RUN ln -s /opt/certbot/bin/certbot /usr/bin/certbot

COPY ./nginx.conf /etc/nginx/conf.d/default.conf
COPY ./enable_https.sh /enable_https.sh


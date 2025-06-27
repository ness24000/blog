# this must 0. install certbot, 1. enable nginx, 2. run certbot 3. reload nginx

apt install python3 python3-dev python3-venv libaugeas-dev gcc
python3 -m venv /opt/certbot/ && /opt/certbot/bin/pip install --upgrade pip
/opt/certbot/bin/pip install certbot certbot-nginx
ln -s /opt/certbot/bin/certbot /usr/bin/certbot
certbot --nginx --non-interactive --agree-tos -m nestor.chulvi@gmail.com -d txtos.eu

nginx -s reload
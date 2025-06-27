# this must 0. install certbot, 1. enable nginx, 2. run certbot 3. reload nginx

certbot certonly --nginx --non-interactive --agree-tos -m nestor.chulvi@gmail.com -d txtos.eu && nginx -s reload && exec "$@"
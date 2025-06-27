FROM nginx

COPY ./nginx.conf /etc/nginx/conf.d/default.conf

ENTRYPOINT ["bash", "enable_https.sh"]
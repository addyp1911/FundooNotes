FROM nginx:latest

ADD nginx.conf /etc/nginx/nginx.conf
RUN mkdir -p /var/www/fundoonote/static

WORKDIR /var/www/fundoonote/static
RUN chown -R nginx:nginx /var/www/fundoonote/static

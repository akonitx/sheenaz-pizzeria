FROM nginx:mainline
SHELL [ "bash", "-c" ]
# need this to make nginx nginx variables substitution correct 
# when using envsubst command
# 
# Example:
# 		proxy_set_header Host $host;
# in this exmaple envsubst comand will substitue nginx variable
# and we don't wanna this.
# 
# Solution:
# 		proxy_set_header Host ${DOLLAR}host;
ENV DOLLAR="$"
# Port that nginx listens
ENV NGINX_SERVER_PORT=80
# server_name directive value 
ENV NGINX_SERVER_HOST=0.0.0.0
# proxy_pass directive value 
ENV NGINX_PROXY_PASS=django:8000
EXPOSE 80/tcp

COPY ./* /etc/nginx/
WORKDIR /etc/nginx/

RUN envsubst < nginx.template > nginx.conf
RUN cat nginx.conf

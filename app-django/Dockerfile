FROM python:3.11-slim-bullseye

SHELL ["bash", "-c"]
EXPOSE 8000/tcp

COPY . /app-django/

WORKDIR /app-django
RUN apt update 
RUN apt install -y libpq5
RUN pip3 install -r requirements.txt


WORKDIR /app-django/lime-root
CMD gunicorn --bind 0.0.0.0:8000 Lime.wsgi --log-level debug


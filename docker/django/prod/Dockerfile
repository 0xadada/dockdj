# AWS Docker container configuration
# Author @0xADADA
# Container OS: Debian Jessie
# Docker: 1.6.2
# Python: 3.4
# Application Server: Gunicorn

FROM            python:3.4

MAINTAINER      @0xADADA

WORKDIR         /var/app

ADD             . /var/app

# Install apt, Python then NodeJS dependencies.
RUN             apt-get update && \
                curl -sL https://deb.nodesource.com/setup_0.12 | bash - && \
                apt-get install -y nodejs && \
                pip install --upgrade pip && \
                pip install -r \
                    environments/prod/requirements.txt && \
                npm update && \
                npm install -g gulp && \
                npm install && \
                gulp build

# Exposes port 8080
EXPOSE          8080

# Add our initialization script to the image and run it upon startup.
ADD             docker/django/start.sh /
ADD             docker/django/prod/gunicorn.conf.py /etc/gunicorn/gunicorn.conf.py
CMD             ["/start.sh"]

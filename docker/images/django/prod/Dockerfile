# AWS Docker container configuration
# Author Ron. A @0xADADA
# Container OS: Debian Jessie
# Docker: 1.6.2
# Python: 3.4
# Application Server: Gunicorn

FROM            python:3.4

MAINTAINER      Ron. A @0xADADA

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
                npm install

# Exposes port 8080
EXPOSE          8080

# Create app log directories and touch log files
RUN             mkdir /var/log/gunicorn && \
                touch /var/log/gunicorn/access.log && \
                touch /var/log/gunicorn/error.log

# Add our initialization script to the image and run it upon startup.
ADD             docker/images/django/start.sh /
ADD             docker/images/nginx/gunicorn.conf.py /etc/gunicorn/gunicorn.conf.py
CMD             ["/start.sh"]

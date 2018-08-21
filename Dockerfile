FROM python:3.6

RUN apt-get update && apt-get install -y postgresql-client

WORKDIR /var/www/lafeeclotilde

COPY . .

ARG app
RUN cd $app && pip install -e .

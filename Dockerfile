FROM python:3.6

RUN apt-get update && apt-get install -y postgresql-client

WORKDIR /var/www/lafeeclotilde

COPY . .

RUN cd common && pip install -e .

ARG app
RUN cd $app && pip install -e .

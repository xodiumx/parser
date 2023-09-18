FROM python:3.11.3-slim-bullseye

RUN apt-get update \
    && apt-get upgrade -y

RUN apt install -y build-essential libpq-dev

WORKDIR /parser_app
COPY . .

RUN pip install --upgrade pip \
    && pip install -r requirements.txt 

RUN ["chmod", "+x", "/parser_app/docker/parser/entrypoint.sh"]

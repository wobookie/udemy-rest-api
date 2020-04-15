FROM python:3.7-alpine
MAINTAINER thiemo.heims@heims-family.com

ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE app.settings

RUN apk add --no-cache --update postgresql-client

# Add build dependencies required to install postgres client
# These are temporary dependencies and removed after requirements installed
RUN apk add --no-cache --update --virtual .tmp-build-deps \
     libc-dev gcc linux-headers postgresql-dev

COPY ./requirements.txt /requirements.txt
RUN pip install -r requirements.txt

# Remove temp dependencies
RUN apk del .tmp-build-deps

RUN mkdir /app
WORKDIR /app
COPY ./app /app

RUN adduser -D nautilus
USER nautilus

EXPOSE 8080
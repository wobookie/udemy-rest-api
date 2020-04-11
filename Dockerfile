FROM python:3.7-alpine
MAINTAINER thiemo.heims@heims-family.com

ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE app.settings

COPY ./requirements.txt /requirements.txt
RUN pip install -r requirements.txt

RUN mkdir /app
WORKDIR /app
COPY ./app /app

RUN adduser -D nautilus
USER nautilus

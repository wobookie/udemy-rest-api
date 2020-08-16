FROM python:3.8-buster
MAINTAINER thiemo.heims

# Set Build Arguments
ARG DJANGO_HOME
ARG DJANGO_USER

# Set Image Environment
ENV PYTHONUNBUFFERED 1

# Install dependencies
COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

# Setup directory structure
RUN mkdir $DJANGO_HOME
COPY ./billywig $DJANGO_HOME

RUN groupadd django \
    && useradd -m -g $DJANGO_USER $DJANGO_USER \
    && chown -R django:django $DJANGO_HOME \
    && chmod ug+x $DJANGO_HOME/bin/startserver.sh

entrypoint "${DJANGO_HOME}/bin/startserver.sh"

USER django
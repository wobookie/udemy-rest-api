#!/bin/sh

echo "starting gunicorn with $DJANGO_WSGI_MODULE:application ... "

gunicorn $DJANGO_WSGI_MODULE:application --workers=3 --bind $APP_ADRPORT --chdir $DJANGO_HOME
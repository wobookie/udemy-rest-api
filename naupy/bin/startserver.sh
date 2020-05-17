#!/bin/sh
echo "prepare application starting ..."
export PYTHONPATH=$DJANGO_HOME:$PYTHONPATH

echo "check db is ready... "
python3 $DJANGO_HOME/manage.py wait_for_db

echo "starting nginx server ... "
nginx

echo "starting gunicorn with $DJANGO_WSGI_MODULE:application in $DJANGO_HOME... "
gunicorn $DJANGO_WSGI_MODULE:application --workers=3 --bind $DJANGO_ADRPORT
# gunicorn $DJANGO_WSGI_MODULE:application --workers=3 --bind $DJANGO_ADRPORT --pythonpath $DJANGO_HOME

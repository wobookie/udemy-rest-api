#!/bin/sh

# NAME="hello_app"                                  # Name of the application
# SOCKFILE=/webapps/hello_django/run/gunicorn.sock  # we will communicte using this unix socket
# USER=hello                                        # the user to run as
# GROUP=webapps                                     # the group to run as
# NUM_WORKERS=3                                     # how many worker processes should Gunicorn spawn
# DJANGO_SETTINGS_MODULE=hello.settings             # which settings file should Django use
# DJANGO_WSGI_MODULE=hello.wsgi                     # WSGI module name
echo "gunicorn ... "

export PYTHONPATH=$DJANGO_HOME:$PYTHONPATH

gunicorn $DJANGO_WSGI_MODULE:application --workers=3 --bind $APP_ADRPORT
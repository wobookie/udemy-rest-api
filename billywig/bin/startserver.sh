#!/bin/sh
echo "prepare application starting ..."
export PYTHONPATH=${DJANGO_HOME}:${PYTHONPATH}

# wait for database to be ready using custom command
echo "wait for database ..."
python ${DJANGO_HOME}/manage.py wait_for_db

# run migrations
echo "run migrations ..."
python ${DJANGO_HOME}/manage.py migrate

# start django sever
echo "start server ..."
python ${DJANGO_HOME}/manage.py runserver 0.0.0.0:${DJANGO_PORT}
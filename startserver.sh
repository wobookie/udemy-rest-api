#!/bin/sh
echo "manage.py wait_for_db..."
python /app/manage.py wait_for_db

echo "manage.py migrate..."
python /app/manage.py migrate

echo "manage.py runnserver... "
python /app/manage.py runserver 0.0.0.0:8080
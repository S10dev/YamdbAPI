#!/usr/bin/env sh

python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --no-input
python manage.py loaddata fixtures.json 

gunicorn api_yamdb.wsgi:application --bind 0.0.0.0:8000 --reload -w 4
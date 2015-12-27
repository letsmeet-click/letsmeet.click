#!/bin/bash
export DJANGO_SETTINGS_MODULE=letsmeet.settings.production
export PYTHONUNBUFFERED=0
mkdir -p /home/uid1000/letsmeet
mkdir -p /home/uid1000/letsmeet/logs
mkdir -p /home/uid1000/letsmeet/run
chmod -R 777 /home/uid1000/letsmeet/run
python3 manage.py migrate
python3 manage.py collectstatic --noinput
gunicorn letsmeet.wsgi:application --log-level=info --bind=unix:/home/uid1000/letsmeet/run/server.sock -w 3

#!/bin/bash

NAME="twito"                                         # Name of the application
DJANGODIR=/home/worker/twito/twito/                  # Django project directory
USER=worker                                          # the user to run as
GROUP=worker                                         # the group to run as
DJANGO_SETTINGS_MODULE=twito.settings

echo "Starting $NAME as `whoami`"

# Activate the virtual environment
cd $DJANGODIR
source ../../venv/bin/activate
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGODIR:$PYTHONPATH

python manage.py celeryd --loglevel=info --concurrency=10 --logfile=logs/django_celery.log

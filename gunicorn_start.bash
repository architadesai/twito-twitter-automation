#!/bin/bash
# still errors

NAME="django_app"                               		   	    	# Name of the application
DJANGODIR=/home/archita/Desktop/twito         				        # Django project directory
SOCKFILE=/home/archita/Desktop/twito/env_twito/run/gunicorn.sock    # we will communicte using this unix socket
USER=archita                                    				        # the user to run as
GROUP=archita                                   				       # the group to run as
NUM_WORKERS=3                                       # how many worker processes should Gunicorn spawn
DJANGO_SETTINGS_MODULE=twito.settings      # which settings file should Django use
DJANGO_WSGI_MODULE=twito.wsgi              # WSGI module name
echo "Starting $NAME as `whoami`"

# Activate the virtual environment

cd $DJANGODIR
source env_twito/bin/activate
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGODIR:$PYTHONPATH

# Create the run directory if it doesn't exist

RUNDIR=$(dirname $SOCKFILE)
test -d $RUNDIR || mkdir -p $RUNDIR

# Start your Django Unicorn
# Programs meant to be run under supervisor should not daemonize themselves (do not use --daemon)

exec gunicorn ${DJANGO_WSGI_MODULE}:application \
  --name $NAME \
  --workers $NUM_WORKERS \
  --user=$USER --group=$GROUP \
  --bind=unix:$SOCKFILE \
  --log-level=debug \
  --log-file=-
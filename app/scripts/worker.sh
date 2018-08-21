#!/bin/bash

# paths
app='/srv/app'
manage=$app'/manage.py'
wsgi=$app'/wsgi.py'

# stating apps
# pip install django-environ redis
pip install south
pip install django-extensions==1.6.7 django-extra-views==0.8.0

# waiting for other services
bash $app/scripts/wait.sh

# Starting celery worker with the --autoreload option will enable the worker to watch for file system changes
# This is an experimental feature intended for use in development only
# see http://celery.readthedocs.org/en/latest/userguide/workers.html#autoreloading
python $manage celery worker --autoreload -A worker

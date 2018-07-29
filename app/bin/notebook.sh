#!/bin/bash

export PYTHONPATH=$PYTHONPATH:/opt/miniconda/lib/python2.7/site-packages/:/srv/app/
export DJANGO_SETTINGS_MODULE=settings

python /srv/app/manage.py shell_plus --notebook

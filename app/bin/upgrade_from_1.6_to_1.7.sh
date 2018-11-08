#!/bin/bash

python manage.py migrate
python manage.py migrate contenttypes --fake-initial
python manage.py migrate --fake-initial
python manage.py migrate thumbnail --fake-initial
python manage.py migrate --fake telemeta 0006

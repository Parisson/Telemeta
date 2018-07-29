#!/bin/bash

app='/srv/app'
manage=$app'/manage.py'

python $manage migrate --noinput
python $manage telemeta-create-admin-user
python $manage telemeta-create-boilerplate
python $manage bower_install -- --allow-root

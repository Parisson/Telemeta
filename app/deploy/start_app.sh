#!/bin/sh

# paths
app='/opt/app'
manage=$app'/manage.py'
wsgi=$app'/wsgi.py'
static='/opt/static/'

# stating apps
# pip install django-haystack elasticsearch

# waiting for other services
sh $app/deploy/wait.sh

# django init
python $manage syncdb --noinput
python $manage migrate --noinput
python $manage collectstatic --noinput
python $manage telemeta-create-admin-user
python $manage telemeta-create-boilerplate
python $manage update_index

# static files auto update
watchmedo shell-command --patterns="*.js;*.css" --recursive \
    --command='python '$manage' collectstatic --noinput' $static &

# app start
uwsgi --socket :8000 --wsgi-file $wsgi --chdir $app --master --processes 4 --threads 2 --py-autoreload 3

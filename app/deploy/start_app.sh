#!/bin/sh

# paths
app='/opt/app'
manage=$app'/manage.py'
wsgi=$app'/wsgi.py'
static='/opt/static/'

# uwsgi params
port=8000
processes=16
threads=2
autoreload=3

# stating apps
pip install redis

# waiting for other services
sh $app/deploy/wait.sh

# django init
python $manage syncdb --noinput
python $manage migrate --noinput
python $manage collectstatic --noinput
python $manage telemeta-create-admin-user
python $manage telemeta-create-boilerplate
#python $manage update_index --workers $processes

# static files auto update
watchmedo shell-command --patterns="*.js;*.css" --recursive \
    --command='python '$manage' collectstatic --noinput' $static &

# app start
uwsgi --socket :$port --wsgi-file $wsgi --chdir $app --master --processes $processes --threads $threads --py-autoreload $autoreload

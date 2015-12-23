#!/bin/sh

# paths
app='/srv/app'
manage=$app'/manage.py'
wsgi=$app'/wsgi.py'
static='/srv/static/'

# uwsgi params
port=8000
processes=8
threads=8
autoreload=3

# stating apps
pip install redis

# waiting for other services
sh $app/deploy/wait.sh

# django init
python $manage syncdb --noinput
python $manage migrate --noinput
python $manage collectstatic --noinput

# static files auto update
watchmedo shell-command --patterns="*.js;*.css" --recursive \
    --command='python '$manage' collectstatic --noinput' $static &

# app start
uwsgi --socket :$port --wsgi-file $wsgi --chdir $app --master --processes $processes --threads $threads --py-autoreload $autoreload

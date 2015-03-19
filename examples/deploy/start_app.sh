#!/bin/sh

# paths
app='/opt/Telemeta/'
static=$app'telemeta/static/'
sandbox='/home/sandbox/'
manage=$sandbox'manage.py'
wsgi=$sandbox'wsgi.py'

sh $app/examples/deploy/wait.sh

# django init
python $manage syncdb --noinput
python $manage migrate --noinput
python $manage collectstatic --noinput
python $manage telemeta-create-admin-user

# static files auto update
pip install watchdog

watchmedo shell-command --patterns="*.js;*.css" --recursive \
    --command='python '$manage' collectstatic --noinput' $static &

# app start
uwsgi --socket :8000 --wsgi-file $wsgi --chdir $sandbox --master --processes 4 --threads 2 --py-autoreload 3

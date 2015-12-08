#!/bin/sh

# paths
app_dir='/opt/Telemeta'
static=$app_dir'/telemeta/static/'
sandbox='/home/sandbox'
manage=$sandbox'/manage.py'
wsgi=$sandbox'/wsgi.py'

# stating apps
pip install django-haystack elasticsearch django-bower

# waiting for other services
sh $app_dir/examples/deploy/wait.sh

# django init
python $manage syncdb --noinput
python $manage migrate --noinput
python $manage bower install --noinput
python $manage collectstatic --noinput
python $manage telemeta-create-admin-user
python $manage telemeta-create-boilerplate
python $manage update_index

# static files auto update
watchmedo shell-command --patterns="*.js;*.css" --recursive \
    --command='python '$manage' collectstatic --noinput' $static &

# app start
uwsgi --socket :8000 --wsgi-file $wsgi --chdir $sandbox --master --processes 4 --threads 2 --py-autoreload 3

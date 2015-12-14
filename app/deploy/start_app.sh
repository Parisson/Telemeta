#!/bin/sh

# paths
app='/opt/app'
manage=$app'/manage.py'
wsgi=$app'/wsgi.py'
static='/opt/static/'

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

if [ ! -f $app/.init ]; then
 python $manage telemeta-create-admin-user
 python $manage telemeta-create-boilerplate
 python $manage update_index --workers $processes
 touch $app/.init
fi

# static files auto update
watchmedo shell-command --patterns="*.js;*.css" --recursive \
    --command='python '$manage' collectstatic --noinput' $static &

# app start
uwsgi --socket :$port --wsgi-file $wsgi --chdir $app --master --processes $processes --threads $threads --py-autoreload $autoreload

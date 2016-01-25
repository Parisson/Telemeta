#!/bin/sh

# paths
app='/srv/app'
manage=$app'/manage.py'
wsgi=$app'/wsgi.py'
static='/srv/static/'
media='/srv/media/'

# uwsgi params
port=8000
processes=8
threads=8
autoreload=3
uid='www-data'
gid='www-data'

# stating apps
pip install django-environ redis

# waiting for other services
sh $app/deploy/wait.sh

# waiting for available database
python $app/wait.py

# django init
python $manage syncdb --noinput
python $manage migrate --noinput
python $manage collectstatic --noinput

if [ ! -f $app/.init ]; then
 chown -R www-data:www-data $media
 python $manage telemeta-create-admin-user
 python $manage telemeta-create-boilerplate
 python $manage update_index --workers $processes &
 touch $app/.init
fi

# static files auto update
watchmedo shell-command --patterns="*.js;*.css" --recursive \
    --command='python '$manage' collectstatic --noinput' $static &

# app start
uwsgi --socket :$port --wsgi-file $wsgi --chdir $app --master \
    --processes $processes --threads $threads \
    --uid $uid --gid $gid \
    --py-autoreload $autoreload

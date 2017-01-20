#!/bin/bash

# paths
app='/srv/app'
manage=$app'/manage.py'
wsgi=$app'/wsgi.py'
static='/srv/static/'
media='/srv/media/'
src='/srv/src/'
log='/var/log/uwsgi/app.log'

# uwsgi params
port=8000
processes=8
threads=8
autoreload=3
uid='www-data'
gid='www-data'

# stating apps
pip install -U django==1.8.17
pip uninstall -y south

# waiting for other network services
sh $app/scripts/wait.sh
python $manage wait-for-db

# initial setup
if [ ! -f .init ]; then
    bash $app/scripts/init.sh
    touch .init
fi

if [ $REINDEX = "True" ]; then
    python $manage rebuild_index --noinput
fi

# fix media access rights
chown www-data:www-data $media
for dir in $(ls $media); do
    if [ ! $(stat -c %U $media/$dir) = 'www-data' ]; then
        chown www-data:www-data $media/$dir
    fi
done

# choose dev or prod mode
if [ "$1" = "--runserver" ]; then
    python $manage runserver 0.0.0.0:8000
else
    python $manage collectstatic --noinput

    # app start
    uwsgi --socket :$port --wsgi-file $wsgi --chdir $app --master \
    --processes $processes --threads $threads \
    --uid $uid --gid $gid --logto $log --touch-reload $wsgi

fi

#!/bin/bash

# paths
app='/srv/app'
manage=$app'/manage.py'
wsgi=$app'/wsgi.py'
static='/srv/static/'
media='/srv/media/'
src='/srv/src/'

# uwsgi params
port=8000
processes=8
threads=8
autoreload=3
uid='www-data'
gid='www-data'
patterns='*.js;*.css;*.jpg;*.jpeg;*.gif;*.png;*.svg;*.ttf;*.eot;*.woff;*.woff2'

# stating apps
# pip install django-bootstrap3==6.2.1

# waiting for other network services
sh $app/scripts/wait.sh

# django setup
python $manage wait-for-db
python $manage syncdb --noinput
python $manage migrate --noinput
python $manage bower_install -- --allow-root

# telemeta setup
python $manage telemeta-create-admin-user
python $manage telemeta-create-boilerplate

# Delete Timeside database if it exists
cat /srv/src/telemeta/scripts/sql/drop_timeside.sql | python $manage dbshell

if [ $REINDEX = "True" ]; then
    python $manage rebuild_index --noinput
fi

# fix media access rights
find $media -path ${media}import -prune -o -type d -not -user www-data -exec chown www-data:www-data {} \;

# choose dev or prod mode
if [ "$1" = "--runserver" ]; then
    python $manage runserver 0.0.0.0:8000
else
    # static files auto update
    # watchmedo shell-command --patterns="$patterns" --recursive \
    #     --command='python '$manage' collectstatic --noinput' $src &

    python $manage collectstatic --noinput

    # app start
    uwsgi --socket :$port --wsgi-file $wsgi --chdir $app --master \
        --processes $processes --threads $threads \
        --uid $uid --gid $gid \
        --py-autoreload $autoreload
fi

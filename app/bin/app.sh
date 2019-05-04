#!/bin/bash

# paths
app='/srv/app'
manage=$app'/manage.py'
wsgi=$app'/wsgi.py'
static='/srv/static/'
media='/srv/media/'
lib='/srv/lib/'
log='/var/log/uwsgi/app.log'

# uwsgi params
port=8000
processes=8
threads=8
uid='www-data'
gid='www-data'

# stating apps
# pip uninstall -y south
# pip install -U django==1.8.18 django-registration-redux djangorestframework==3.6.4
# pip install django-debug-toolbar==1.6
# pip install -e git+https://github.com/Parisson/django-jqchat.git@dj1.8#egg=django-jqchat
# pip install -e git+https://github.com/Parisson/saved_searches.git@dj1.8#egg=saved_searches-2.0.0-beta

# waiting for other network services
sh $app/bin/wait.sh
python $manage wait-for-db

if [ ! -f .init ]; then
    python $manage migrate --noinput
    python $manage bower_install -- --allow-root
    touch .init
fi

# telemeta setup
python $manage telemeta-create-admin-user
python $manage telemeta-create-boilerplate
python $manage telemeta-setup-enumerations


# Delete Timeside database if it exists
cat /srv/lib/telemeta/bin/sql/drop_timeside.sql | python $manage dbshell

if [ $REINDEX = "True" ]; then
    python $manage rebuild_index --noinput
fi

# choose dev or prod mode
if [ "$1" = "--runserver" ]; then
    python $manage runserver 0.0.0.0:8000
else
    # static files auto update
    # watchmedo shell-command --patterns="$patterns" --recursive \
    #     --command='python '$manage' collectstatic --noinput' $lib &
    python $manage collectstatic --noinput

    # fix media access rights
    find $media -maxdepth 2 -path ${media}import -prune -o -type d -not -user www-data -exec chown www-data:www-data {} \;

    # app start
    uwsgi --socket :$port --wsgi-file $wsgi --chdir $app --master \
        --processes $processes --threads $threads \
        --uid $uid --gid $gid --logto $log --touch-reload $wsgi
fi

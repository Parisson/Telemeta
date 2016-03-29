#!/bin/sh

# paths
app='/srv/app'
manage=$app'/manage.py'
wsgi=$app'/wsgi.py'
static='/srv/static/'
media='/srv/media/'
src='/srv/src/'

chown www-data:www-data $media

# uwsgi params
port=8000
processes=8
threads=8
autoreload=3
uid='www-data'
gid='www-data'

# stating apps
pip install --upgrade pip
pip install -U django==1.6.11 django-environ redis django-angular
pip install -U git+https://github.com/Parisson/saved_searches.git#egg=saved_searches-2.0.0-beta

# waiting for other services
sh $app/deploy/wait.sh

# waiting for available database
python $app/wait.py

# django init
python $manage syncdb --noinput
python $manage migrate --noinput
python $manage bower_install -- --allow-root
python $manage collectstatic --noinput
python $manage telemeta-create-admin-user
python $manage telemeta-create-boilerplate

if [ $DEBUG = "False" ]
then
    python $manage update_index --workers $processes &
fi

if [ $1 = "--runserver" ]
then
    python $manage runserver_plus 0.0.0.0:8000
else
    # static files auto update
    watchmedo shell-command --patterns="*.js;*.css" --recursive \
        --command='python '$manage' collectstatic --noinput' $src &

    # app start
    uwsgi --socket :$port --wsgi-file $wsgi --chdir $app --master \
        --processes $processes --threads $threads \
        --uid $uid --gid $gid \
        --py-autoreload $autoreload
fi

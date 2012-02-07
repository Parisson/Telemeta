#!/bin/sh

cd telemeta
django-admin makemessages -a
django-admin makemessages -d djangojs -a
django-admin compilemessages
cd ..

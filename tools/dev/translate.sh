#!/bin/sh

cd telemeta
django-admin.py makemessages -a
django-admin.py makemessages -d djangojs -a
django-admin.py compilemessages
cd ..

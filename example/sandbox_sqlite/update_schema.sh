#!/bin/sh

./manage.py schemamigration telemeta --auto
./manage.py migrate telemeta


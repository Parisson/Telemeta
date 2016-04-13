#!/bin/bash

./manage.py schemamigration telemeta --auto
./manage.py migrate telemeta

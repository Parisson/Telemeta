#!/bin/bash

gunzip < /srv/backup/$1 | mysql -hdb -uroot -pmysecretpassword telemeta

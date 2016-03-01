#!/bin/bash

PASSWORD=$1
NOW=$(date +"%Y-%m-%d-%T")

mysqldump -hdb -uroot -p$PASSWORD telemeta | gzip > /srv/backup/telemeta-$NOW.sql.gz

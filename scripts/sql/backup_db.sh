#!/bin/bash

NOW=$(date +"%Y-%m-%d-%T")

mysqldump -hdb -uroot -p$MYSQL_ROOT_PASSWORD telemeta | gzip > /srv/backup/telemeta-$NOW.sql.gz

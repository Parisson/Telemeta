#!/bin/bash

NOW=$(date +"%T-%m-%d-%Y")
mysqldump -hdb -uroot -pmysecretpassword telemeta | gzip > /srv/backup/telemeta-$NOW.sql.gz

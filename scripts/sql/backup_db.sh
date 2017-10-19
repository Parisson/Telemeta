#!/bin/bash

DIR=/srv/backup/
NOW=$(date +"%Y-%m-%d-%T")
FILE=telemeta-$NOW.sql.gz

echo "Backuping: "$FILE

mysqldump -hdb -uroot -p$MYSQL_ROOT_PASSWORD telemeta | gzip > $DIR$FILE

rename 's/\:/\_/g' $DIR$FILE

echo "Done!"

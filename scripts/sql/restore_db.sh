#!/bin/bash

PASSWORD=$1
DIR=/srv/backup/
FILE=`ls -t $DIR/*.sql* | head -1`

if [[ $FILE == *".gz" ]]; then
    gunzip < $FILE | mysql -hdb -uroot -p$PASSWORD telemeta
else
    mysql -hdb -uroot -p$PASSWORD telemeta < $FILE
fi

echo "backup restored : "$FILE

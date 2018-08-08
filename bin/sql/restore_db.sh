#!/bin/bash

DIR=/srv/backup/
FILE=`ls -t $DIR/*.sql* | head -1`

echo "Restoring: "$FILE

if [[ $FILE == *".gz" ]]; then
    gunzip < $FILE | mysql -hdb -uroot -p$MYSQL_ROOT_PASSWORD telemeta
else
    mysql -hdb -uroot -p$MYSQL_ROOT_PASSWORD telemeta < $FILE
fi

echo "Done!"

#!/bin/bash

file=$1

if [[ $file == *".gz" ]]; then
    echo 'ok'
    gunzip < /srv/backup/$file | mysql -hdb -uroot -pmysecretpassword telemeta
else
    mysql -hdb -uroot -pmysecretpassword telemeta < /srv/backup/$file
fi

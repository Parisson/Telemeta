#!/bin/sh
# needs epydoc

app="telemeta"
dir=/home/$USER/dev/$app/doc/
server="angus.parisson.com"

epydoc -n $app -u https://github.com/yomguy/Telemeta -o $dir $app/
rsync -a $dir $server:/var/www/files/doc/$app/


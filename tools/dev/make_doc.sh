#!/bin/sh
# needs epydoc

app="telemeta"
dir=/home/$USER/dev/$app/doc/
server="git.parisson.com"

epydoc -n $app -u https://github.com/Parisson/Telemeta -o $dir $app/
rsync -a $dir $server:/var/www/files/doc/$app/


#!/bin/sh
# needs epydoc

app="telemeta"
dir=/home/$USER/dev/$app/doc/
server="angus.parisson.com"

epydoc -n $app -u https://github.com/yomguy/DeeFuzzer -o $dir $app/
rsync -a --delete $dir $server:/var/www/files/doc/$app/


#!/bin/bash

plugins=/srv/lib/plugins

for dir in $(ls $plugins); do
    if [ -f $plugins/$dir/setup.py ]; then
        pip install -e $plugins/$dir/.
    fi
done

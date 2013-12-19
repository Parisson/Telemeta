#!/bin/sh

#threads=$1
dir=$1

for file in `ls $dir/*.sh`; do
 perl -pi -e 's/threads=6/threads=4/g' $file
 perl -pi -e 's/threads=2/threads=4/g' $file
 perl -pi -e 's/threads=1/threads=4/g' $file
done

#!/bin/sh

threads=$1
dir=$2

for file in `ls $dir/*.sh`; do
 perl -pi -e 's/threads=2/threads=$threads/g' $file
 perl -pi -e 's/threads=4/threads=$threads/g' $file
 perl -pi -e 's/threads=6/threads=$threads/g' $file
done

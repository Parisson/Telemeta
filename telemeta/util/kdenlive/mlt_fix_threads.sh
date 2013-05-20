#!/bin/sh

for file in `ls $1/*.sh`; do
perl -pi -e 's/threads=2/threads=8/g' $file
perl -pi -e 's/threads=4/threads=8/g' $file
perl -pi -e 's/threads=6/threads=8/g' $file
done

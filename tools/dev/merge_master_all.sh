#!/bin/bash

git branch | tr -d \* | while read line
do
    branch=${line/#\ }

    if [[ ! $branch == *master* ]]; then
     echo "Merge master to $branch:"
     git checkout $branch
     git merge master
     git checkout master
    fi
done

echo "Done !"

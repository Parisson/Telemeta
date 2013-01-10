#!/bin/bash

git branch | tr -d \* | while read line
do
    branch=${line/#\ }

    echo "Push $branch to origin:"
    git push origin $branch

    echo "Push $branch to github:"
    git push hub $branch

done

git push --tags
git push --tags hub

ssh vcs.parisson.com "cd /var/git/telemeta.git; git update-server-info"

#echo "Update jimi.parisson.com:"
echo "Update angus.parisson.com:"
ssh angus.parisson.com "cd /home/telemeta/telemeta-master; git pull origin master; \
                        cd /home/telemeta/telemeta-develop; git pull origin dev; \
                        cd /home/telemeta/demo/; ./manage.py migrate --delete-ghost-migrations;
                        cd /home/telemeta/sandbox/; ./manage.py migrate --delete-ghost-migrations; 
                        cd /home/telemeta/parisson/; ./manage.py migrate --delete-ghost-migrations; "

echo "Done !"

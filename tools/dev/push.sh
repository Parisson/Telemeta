#!/bin/bash

git branch | tr -d \* | while read line
do
    branch=${line/#\ }

    git push origin $branch
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

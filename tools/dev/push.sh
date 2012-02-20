#!/bin/bash

git branch | tr -d \* | while read line
do
    branch=${line/#\ }

    echo "Push $branch to origin:"
    git push origin $branch

    echo "Push $branch to web:"
    git push web $branch

    if [[ $branch == *master* ]]; then
        echo "Push $branch to github:"
        git push github $branch
    fi

done

git push --tags
git push --tags web
git push --tags github

ssh vcs.parisson.com "cd /var/git/telemeta.git; git update-server-info"
ssh vcs.parisson.org "cd /var/git/telemeta.git; git update-server-info"

#echo "Update jimi.parisson.com:"
#ssh jimi.parisson.com "cd /home/telemeta/telemeta; git pull origin production"
echo "Update angus.parisson.com:"
ssh angus.parisson.com "cd /home/telemeta/telemeta-prod; git pull origin production; \
                        cd /home/telemeta/telemeta; git pull origin master; \
                        cd /home/telemeta/demo/; ./manage.py migrate telemeta --delete-ghost-migrations;
                        cd /home/telemeta/sandbox/; ./manage.py migrate telemeta --delete-ghost-migrations; "

echo "Done !"

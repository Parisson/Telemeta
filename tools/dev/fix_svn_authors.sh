
git filter-branch -f --commit-filter '
        if [ "$GIT_COMMITTER_EMAIL" = "<>" ];
        then
                GIT_COMMITTER_NAME="<yomguy>";
                GIT_AUTHOR_NAME="<yomguy>";
                GIT_COMMITTER_EMAIL="<yomguy@parisson.com>";
                GIT_AUTHOR_EMAIL="<yomguy@parisson.com>";
                git commit-tree "$@";
        else
                git commit-tree "$@";
        fi' HEAD

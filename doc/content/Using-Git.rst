Telemeta project now uses Git for development
##############################################

:category: Development
:date: 2011-10-26 06:53
:tags: git

Ten months ago, I started to look at other version control systems because I was fed up with the Subversion centralized model. It tested Git, Mercurial, Bazaar, etc.. Bazaar was the good choice because it allowed the dev teams to make branches easily in a decentralized environment, to push commits to the old subversion repository, to keep an easy syntax, etc...

Now there are few reasons to switch back to Git:

we want to checkout and test branches faster without managing dozens of repositories,
we do not want to upload 500 ko of data for a 1 line commit,
we want to push the generic Telemeta to GitHub.
Sorry Bzr folks, I like your stuff, but Git is more appropriate now for this project.

Developers, please ​`update your skills <http://schacon.github.com/git/gittutorial.html>`_ :)

What you need to do with the new repository:

* Get the lastest development version to try the lastest useful features ::

    git clone http://vcs.parisson.com/git/telemeta.git

* To get the CREM's branch::

    git clone http://vcs.parisson.com/git/telemeta.git
    git checkout crem

* You can also ​follow / fork the `project on GitHub <https://github.com/yomguy/Telemeta>`_ !
* To get write access to the main repository (i.e. ​git+ssh://vcs.parisson.com/var/git/telemeta.git), please contact us by email.

NB : ​This is the good method to convert a Bzr repo.
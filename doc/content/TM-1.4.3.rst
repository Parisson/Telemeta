Telemeta 1.4.3 has been released !
##################################

:category: Release
:date: 2012-05-31 22:57

Changes:

* add solr-thumbnail for automatic thumbnail handling of all related media images (please install)
* add static media handling for solr and all various telemeta public files
* fix some wrong user properties
* SECURITY: you need to move your TELEMETA_EXPORT_CACHE_DIR from TELEMETA_CACHE_DIR cache (see example/sandbox_sqlite/settings.py)
* EXPERIMENTAL: WebM and MP4 video handling for items, NO transcode but decode, add a nice video.js player
* RECOMMEND: install django-extensions
* add user revisions to user profile
* move all edit buttons to main edit pages
* new Format object and various enumerations
* add last revision to item detail
* various bugfixes
* Fix a bug for related media title parsing

Upgrade::

    sudo pip install --upgrade telemeta

or `download <​​http://pypi.python.org/packages/source/T/Telemeta/Telemeta-1.4.3.tar.gz>`_ (MD5: ceec77f9b5e637cf1e2cb9b9fad21183)

As usual, please first read README.rst and INSTALL.rst to get all informations about the news. Apply new rules, dependencies, modules and settings from your old version to the new one.

For example, you now need sorl-thumbnail to get image thumbnails::

    sudo pip install sorl-thumbnail

and add 'sorl.thumbnail' to your INSTALLED_APPS list in settings.py.

When all new settings seem OK, use ​South for a clean data migration from previous model versions::

    ./manage.py syncdb
    ./manage.py migrate telemeta

email me or tweet to @telemeta if any problem.

Enjoy!


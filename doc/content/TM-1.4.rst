Telemeta 1.4 is out!
#####################

:category: Release
:date: 2012-02-14 16:29

Changes:

* add a Desk providing links to home and personal data
* add Fonds, Corpus and their related media to the models and to the search engine
* add some fancy drop down menus for main tabs
* add video media handling (WebM formats only and with the last TimeSide master branch)
* add playlist metadata editor
* fix some sad bugs for YouTube related URLs and previews
* cleanup admin page
* add auto saving now for all searches !
* add "My Searches" modules to user lists with search direct link
* add RSS feeds for last changes of all users
* better icon views
* many bugfixes !

For developers and maintainers:

* a new setting parameter: TELEMETA_DOWNLOAD_FORMATS = ('wav', 'mp3', 'webm') or whatever
* before upgrading, you need to BACKUP and manually delete old wrong MediaCorpus? and MediaCorpusRelated? tables
* we now use South for data model migration. Add 'south' to your apps and to do::

    ./manage.py syncdb
    ./manage.py migrate telemeta

Upgrade::

    sudo pip install --upgrade telemeta

or `download <​​http://pypi.python.org/packages/source/T/Telemeta/Telemeta-1.4.tar.gz>`_ (MD5: ec51039d0b749f8322309c64e9415090)

Please first read README.rst and INSTALL.rst to get all informations about the news. Apply new rules, dependencies, modules and settings from your old version to the new one.

Enjoy!


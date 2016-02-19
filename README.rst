=================================================
Telemeta: open web audio platform with semantics
=================================================

|version| |downloads| |travis_master| |coverage_master|

.. |version| image:: https://img.shields.io/pypi/v/telemeta.svg
   :target: https://pypi.python.org/pypi/Telemeta/
   :alt: Version

.. |downloads| image:: https://img.shields.io/pypi/dm/telemeta.svg
   :target: https://pypi.python.org/pypi/Telemeta/
   :alt: Downloads

.. |travis_master| image:: https://secure.travis-ci.org/Parisson/Telemeta.png?branch=master
   :target: https://travis-ci.org/Parisson/Telemeta/
   :alt: Travis

.. |coverage_master| image:: https://coveralls.io/repos/Parisson/Telemeta/badge.png?branch=master
   :target: https://coveralls.io/r/Parisson/Telemeta?branch=master
   :alt: Coverage


Overview
=========

Telemeta is a free and open source web audio archiving software which introduces useful and secure methods to backup, index, transcode, analyse and publish any digitalized audio file with extensive metadata. It is dedicated to collaborative media archiving projects, research laboratories and digital humanities - and especially in ethnomusicological use cases - who wants to easily organize, backup and publish documented sound collections of audio files, CDs, digitalized vinyls and magnetic tapes over a strong database, in accordance with open web standards.

Key features:

* Secure archiving, editing and publishing of audio files over internet.
* Pure HTML web user interface including dynamical forms and smart workflows
* Smart dynamical and skinnable audio player (thanks to  TimeSide and  SoundManager2)
* "On the fly" audio analyzing, transcoding and metadata embedding based on an easy plugin architecture
* Social cumulative indexing with semantic ontologies and timecoded markers
* Multi-format support : FLAC, OGG, MP3, WAV and more
* User management with individual desk, lists, profiles and rights
* Playlist management for all users with CSV data export
* Geo-Navigator for audio geolocalization
* High level search engine
* DublinCore compatibility
* OAI-PMH data provider
* RSS feed generators
* XML and ZIP serialized backups
* SQLite, MySQL, PostgreSQL or Oracle DB backends
* Multi-language support (now english and french)
* Video support (EXPERIMENTAL, WebM only)

This web audio CMS is exclusively based on open source modules and can be run on any Unix or Linux system.
It is mostly written in Python and JavaScript.

The processing engine of Telemeta is a separate project called `TimeSide <https://github.com/yomguy/timeside/>`_ as an open web audio pocessing framework written in Python.


Changes
========

1.6
++++

* Provide a docker image and composition for the full Telemeta bundle
* Full refactoring of the search engine and interface using django-haystack with new faceting and filtering features
* Add an EPUB3 ebook exporter for corpus and collections embedding metadata, image and audio materials.
* Many bugfixes

1.5.1
++++++

* Fix geo-navigator lists and pagination
* Fix item analyses cleanup after file edit
* Fix performance and keywords copy during item copy
* Add various annotation mime types (ELAN, Trancriber, Sonic Visualizer)
* Add arabic translations through Telemeta-locales (thanks to @AnasGhrab)
* Fix arabic and chinese codes in sandbox
* Better locale / pages management
* A better management of RTL for arabic page style

`More changes <http://parisson.github.io/Telemeta/category/releases.html>`_.


Examples
========

* `Sound archives of the French Ethnomusicology Research Center (CREM) and the Musée de l'Homme <http://archives.crem-cnrs.fr>`_ :

* a 120 year old ethnomusicologic database,
* more than 5000 geolocated collections,
* more than 32000 geolocated items,
* more than 11000 sounds included
* 1.5 To of original music files accessible online.
* started in june 2011

* `Sound archives of the team "Lutherie, Acoustique et Musique" (LAM) of the IJLRDA institute - University Pierre et Marie Curie (Paris 6) <http://telemeta.lam.jussieu.fr>`_ :

* original musical instruments recorded for research purposes
* started in sept. 2012

* `Sound archives of Parisson Studio <http://parisson.telemeta.org>`_

* `Scaled BIOdiversity (SABIOD) <http://sabiod.telemeta.org>`_


Demo
====

http://demo.telemeta.org

login: demo
password: demo


Install
=======

Thanks to Docker, Telemeta is now fully available as a docker image ready to work. The docker based composition bundles some powerfull applications and modern frameworks out-of-the-box like: Python, Numpy, Gstreamer, Django, Celery, Haystack, ElasticSearch, MySQL, RabbitMQ, uWSGI, Nginx and many more...

First install `Git <http://git-scm.com/downloads>`_, `Docker <https://docs.docker.com/installation/>`_ and `docker-compose <https://docs.docker.com/compose/install/>`_, then run these commands in a terminal::

    git clone --recursive https://github.com/Parisson/Telemeta.git
    cd Telemeta
    docker-compose up

You can now browse http://localhost:8000


Restore / backup
================

To restore a backuped database, put your backup file in data/backup, then in another terminal::

    docker-compose run db /srv/backup/restore_db.sh FILENAME

where FILENAME is the backup filename (can be .sql or .sql.gz)

To backup the database, just run in another terminal::

    docker-compose run db /srv/backup/backup_db.sh


API / Documentation
====================

* Official website: http://telemeta.org
* Publications : https://github.com/Parisson/Telemeta-doc
* API : http://files.parisson.com/doc/telemeta/
* Player : https://github.com/Parisson/TimeSide/
* Example : http://archives.crem-cnrs.fr/archives/items/CNRSMH_E_2004_017_001_01/


Related software projects
==========================

* `TimeSide <https://github.com/yomguy/timeside/>`_: high level python audio processing framework
* `Diadems <http://www.irit.fr/recherches/SAMOVA/DIADEMS/fr/welcome/&cultureKey=en>`_ Description, Indexation, Access to Sound and Ethnomusicological Documents, funded by the French Research Agency (ANR CONTINT 2012)
* `TimeSide-Diadems <https://github.com/ANR-DIADEMS/timeside-diadems>`_: a set of Timeside plugins developed during the Diadems project


Development
===========

|travis_dev| |coverage_dev|

.. |travis_dev| image:: https://secure.travis-ci.org/Parisson/Telemeta.png?branch=dev
   :target: https://travis-ci.org/Parisson/Telemeta/
   :alt: Travis

.. |coverage_dev| image:: https://coveralls.io/repos/Parisson/Telemeta/badge.png?branch=dev
   :target: https://coveralls.io/r/Parisson/Telemeta?branch=dev
   :alt: Coverage


You are welcome to participate to the development of the Telemeta project which is hosted on `GitHub <https://github.com/Parisson/Telemeta>`_.

The development package and environment is available through our `DevBox <https://github.com/Parisson/DevBox>`_


Bugs and feedback
=================

You are welcome to freely use this application in accordance with its licence.

If you find some bugs or have good ideas for enhancement, please leave a issue on GitHub with the right label:

https://github.com/Parisson/Telemeta/issues/new

You can also leave some ticket to request some new interesting features for the next versions and tweet your ideas to `@telemeta <https://twitter.com/telemeta>`_.

And even if Telemeta suits you, please give us some feedback !


Contact
=======

Homepage: http://telemeta.org

Emails:

* Guillaume Pellerin <yomguy@parisson.com>,
* Thomas Fillon <thomas@parisson.com>
* Anas Ghrab <anas.ghrab@gmail.com>
* Olivier Guilyardi <olivier@samalyse.com>,
* Riccardo Zaccarelli <riccardo.zaccarelli@gmail.com>

Twitter:

* https://twitter.com/telemeta
* https://twitter.com/parisson_studio
* https://twitter.com/yomguy


License
=======

CeCILL v2, compatible with GPL v2 (see `LICENSE <http://github.com/yomguy/Telemeta/blob/master/LICENSE.txt>`_)

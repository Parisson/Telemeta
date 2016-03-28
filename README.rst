=================================================
Collaborative multimedia asset management system
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

Telemeta is a free and open source collaborative multimedia asset management software which introduces useful and secure methods to archive, backup, transcode, analyse,  annotate and publish any digitalized video or audio file with extensive metadata. It is dedicated to collaborative media archiving projects, research laboratories and digital humanities - especially in ethno-musicological use cases - who need to easily organize and publish documented sound collections of audio files, CDs, digitalized vinyls and magnetic tapes over a strong database, in a secure platform and in accordance with open web standards.

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

The processing engine of Telemeta is provided by `TimeSide <https://github.com/yomguy/timeside/>`_, an open web audio processing framework written in Python.


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

Thanks to Docker, Telemeta is now fully available as a docker composition ready to work. The docker based composition bundles some powerfull applications and modern frameworks out-of-the-box like: Python, Numpy, Gstreamer, Django, Celery, Haystack, ElasticSearch, MySQL, Redis, uWSGI, Nginx and many more.

On Linux, first install `Git <http://git-scm.com/downloads>`_, `Docker engine <https://docs.docker.com/installation/>`_ and `docker-compose <https://docs.docker.com/compose/install/>`_ and open a terminal.

On MacOSX or Windows install the `Docker Toolbox <https://www.docker.com/products/docker-toolbox>`_ and open a Docker Quickstart Terminal.

Then run these commands::

    git clone --recursive https://github.com/Parisson/Telemeta.git
    cd Telemeta
    docker-compose up db

Press CTRL-C to exit (the last command is needed to init the database).

Start
=====

For a production environment setup::

     docker-compose up

Then browse the app at http://localhost:8000/ (replacing 'localhost' by the IP given by the docker terminal on OSX or Windows)

For a development environment setup::

    docker-compose -f docker-compose.yml -f env/dev.yml up

Then browse the app at http://localhost:9000/ (replacing 'localhost' by the IP given by the docker terminal on OSX or Windows)

To start the application in DEBUG mode::

    docker-compose -f docker-compose.yml -f env/debug.yml up


Backup / Restore
================

To backup the database in the data/backup/ folder, run this in **another** terminal (or a Docker Quickstart Terminal)::

    docker-compose run db /srv/scripts/sql/backup_db.sh

To restore the last backuped database from the data/backup/ folder, run this in **another** terminal (or a Docker Quickstart Terminal)::

    docker-compose run db /srv/scripts/sql/restore_db.sh

If the app is broken after a restore script, restart the composition with::

    docker-compose restart


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


License
=======

This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License along with this program. If not, see <http://www.gnu.org/licenses/>.

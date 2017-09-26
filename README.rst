============================================================
Telemeta : collaborative multimedia asset management system
============================================================

.. image:: https://raw.githubusercontent.com/Parisson/Telemeta/master/telemeta/static/telemeta/images/logo_telemeta_2.png
    :alt: Telemeta logo

Overview
=========

Telemeta is a free and open source collaborative multimedia asset management system (MAM) which introduces fast and secure methods to archive, backup, transcode, analyse,  annotate and publish any digitalized video or audio file with extensive metadata. It is dedicated to collaborative media archiving projects, research laboratories and digital humanities - especially in ethno-musicological use cases - who need to easily organize and publish documented sound collections of audio files, CDs, digitalized vinyls and magnetic tapes over a strong database, through a smart and secure platform, in accordance with open web standards.

Key features:

* Secure archiving, editing and publishing of audio files over internet.
* Pure HTML web user interface including dynamical forms and smart workflows
* "On the fly" audio analyzing and transcoding thanks to TimeSide_
* Smart dynamical and skinnable audio player with annotations
* Collaborative indexing with semantic ontologies and timecoded markers
* Multi-format support : FLAC, OGG, MP3, WAV, MP4, WebM (video) and more
* User management with individual desk, lists, profiles and rights
* Playlist management for all users with CSV data export
* Geo-Navigator for audio geolocalization
* High level search engine
* DublinCore compatibility
* OAI-PMH data provider
* RSS feed generators
* XML and ZIP serialized backups
* EPUB3 "audio book" collection exporter
* SQLite, MySQL, PostgreSQL or Oracle DB backends
* Multi-language support (now english and french)
* Run on any OS

Telemeta has been developed since 2006 and is based exclusively on 100% open source modules.

It is mostly written in Python, HTML5 and JavaScript.

The *Telemeta* name stands for *Tele* as "remote access" and *meta* for "metadata".

|version| |downloads| |travis_master| |coverage_master|

.. |version| image:: https://img.shields.io/pypi/v/telemeta.svg
   :target: https://pypi.python.org/pypi/Telemeta/
   :alt: Version

.. |travis_master| image:: https://secure.travis-ci.org/Parisson/Telemeta.png?branch=master
   :target: https://travis-ci.org/Parisson/Telemeta/
   :alt: Travis

.. |coverage_master| image:: https://coveralls.io/repos/Parisson/Telemeta/badge.png?branch=master
   :target: https://coveralls.io/r/Parisson/Telemeta?branch=master
   :alt: Coverage


Funding and support
===================

To fund this long time libre and open source project, we need your explicit support. So if you use Telemeta in production or even in a development or experimental setup, please let us know by:

* staring or forking the project on GitHub_
* tweeting something to `@parisson_studio <https://twitter.com/parisson_studio>`_ or `@telemeta <https://twitter.com/telemeta>`_
* drop us an email <support@parisson.com>

Thank you so much for your help!


News
=====
1.6.4
+++++
   * Minor bug fixes and improvments
   * Fix HTML5 audio compatibility (#173) for the web audio player. The SoundManager Flash player fallback should not be used in most modern web browser. Media files are now serves through Nginx (#155) which enables to stream music with byte range requests.
   * Add a User permission "can_run_analysis" to specify that a user or a group of users has the right to list and select advanced Timeside analysis to be displayed in the Timeside web audio player.
   * Add enumeration management and statitics
   * Improved media security allowing streaming through Nginx only from the application
   * Add TimeSide as a submodule
   * Add a validator for Corpus and Fonds
   * Upgrade various dependencies

1.6
++++

Telemeta is now usable on **any OS**, ready for development and for production in 5 mn! B-)

* Provide a docker image and composition for the full Telemeta application bundle.
  One month after the publication of docker-compose around march 2015, we had managed to build a prototyped composition which bundled all the dependencies of Telemeta and TimeSide. It took almost one year to deeply investigate all the capabilities of Docker and various images to finally release a propoer composition which bundles all the necessary applications and modules.
* Full refactoring of the search engine and interface using django-haystack and ElasticSearch with new faceting and smart filtering features
* Add an automatic EPUB3 ebook exporter for corpus and collections embedding metadata, image and audio materials.
* More inline forms and functional buttons
* Install new useful tools and modules like Conda, Jupyter notebook and `many others <https://github.com/Parisson/TimeSide/blob/master/conda-requirements.txt>`_
* Add resource sharing links
* Switch to Affero GPL licence
* Upgrade of every dependency bundle in the composition
* Many, many `bugfixes <https://github.com/Parisson/Telemeta/issues?q=is%3Aissue+is%3Aclosed>`_
* Thanks to all partners for this **huge** release!

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

* `CREM Sound archives <http://archives.crem-cnrs.fr>`_ of the CREM_ - CNRS_  and MdH_
* `LAM Sound archives <http://telemeta.lam.jussieu.fr>`_ of the LAM_ of the IJLRDA_ at Université Pierre et Maris Curie (UPMC_)
* `Phonothèque Nationale <http://phonotheque.cmam.tn/>`_ du Centre des Musiques Arabes et Méditerranéennes (CMAM_)
*  Scaled BIOdiversity (SABIOD_)


Demo
====

http://demo.telemeta.org

 * login: admin
 * password: admin


Install
=======

Thanks to Docker, Telemeta is now fully available as a docker composition ready to work. The docker based composition bundles some powerfull applications and modern frameworks out-of-the-box like: Python, Conda, Numpy, Jupyter, Gstreamer, Django, Celery, Haystack, ElasticSearch, MySQL, Redis, uWSGI, Nginx and many more.

* on **Linux**, first install `Git <http://git-scm.com/downloads>`_, `Docker engine <https://docs.docker.com/installation/>`_ (>=1.9) and `docker-compose <https://docs.docker.com/compose/install/>`_ (>=1.8) and open a terminal.
* on **MacOSX** or **Windows** install the `Docker Toolbox <https://www.docker.com/products/docker-toolbox>`_ and open a **Docker Quickstart Terminal**.

Then clone Telemeta::

    git clone --recursive https://github.com/Parisson/Telemeta.git
    cd Telemeta


Start it up
===========

For a production environment setup, first read / edit `env/prod.env`, then::

    docker-compose up

Then browse the app at http://localhost:8000/ (replacing 'localhost' by the IP given by the docker terminal on OSX or Windows)

To start the application in DEBUG mode::

    docker-compose -f docker-compose.yml -f env/debug.yml up

Be **CAREFULL** in production:

* The database is deleted when using `docker-compose rm`
* Define your own passwords and secret keys in `env/*.env` files
* Use a cron rule and the backup script to save your work periodically


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


Development
===========

|travis_dev| |coverage_dev|

.. |travis_dev| image:: https://secure.travis-ci.org/Parisson/Telemeta.png?branch=dev
   :target: https://travis-ci.org/Parisson/Telemeta/
   :alt: Travis

.. |coverage_dev| image:: https://coveralls.io/repos/Parisson/Telemeta/badge.png?branch=dev
   :target: https://coveralls.io/r/Parisson/Telemeta?branch=dev
   :alt: Coverage


To start the application in a development environment setup, first read / edit `env/debug.env`, then::

    cd Telemeta
    git pull
    git checkout dev
    docker-compose -f docker-compose.yml -f env/dev.yml up

Then browse the app at http://localhost:9000/ (replacing 'localhost' by the IP given by the docker terminal on OSX or Windows). Note that the service will automatically be reloaded when any code of the app is modified.

You are welcome to participate to the development by forking the Telemeta project on GitHub_, using it as if it were the original and submitting your changes through a Pull Request on the **dev branch ONLY**.


Bugs, issues, ideas
===================

If you find some bugs or have good ideas for enhancement, please `leave a issue on GitHub <https://github.com/Parisson/Telemeta/issues/new>`_ with the right label or tweet it `@telemeta <https://twitter.com/telemeta>`_.

And remember: even if Telemeta suits you, please give us some feedback. We **need** your support!


License
=======

This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License along with this program. If not, see <http://www.gnu.org/licenses/>.


Sponsors and partners
======================

* CNRS_ : Centre National de la Recherche Scientifique (French Natianal Research and Scientific Center)
* MCC_ : Ministère de la Culture et de la Communication (the french Ministry of the Culture and Communication)
* ANR_ : Agence Nationale de la Recherche (French Research Agency)
* UPMC_ : University Pierre et Marie Curie (Paris 6, Sorbonne Universités, France)
* CREM_ : Centre de Recherche en Ethnomusicologie (Ethnomusicology Research Center, Paris, France)
* LAM_ : Equipe Lutherie, Acoustique et Musique de l'IJLRDA_ (Paris, France)
* IJLRDA_ : Institut Jean le Rond d'Alembert (Paris, France)
* Parisson_ : Open development agency for audio science and arts (Paris, France)
* MNHN_ : Museum National d'Histoire Naturelle (National Museum of Biology, Paris, France)
* U-Paris10_ : University Paris 10 Ouest Nanterre (Nanterre, France)
* MdH_ : Musée de l'Homme (Paris, France)
* IRIT_ : Institut de Recherche en Informatique de Toulouse (Toulouse, France)
* LIMSI_ : Laboratoire d'Informatique pour la Mécanique et les Sciences de l'Ingénieur (Orsay, France)
* LABRI_ : Laboratoire Bordelais de Recherche en Informatique (Bordeaux, France)
* C4DM_ : Centre for Digital Music at `Queen Mary University`_ (London, UK)
* HumaNum_ : TGIR des humanités numériques (Paris, France)
* CMAM_ : Centre des Musiques Arabes et Méditerranéennes (Tunis, Tunisia)
* IRCAM_ : Institut de Recherche et de Coordination Acoustique / Musique (Paris, France)


Related research projects
==========================

* DIADEMS_ : Description, Indexation, Access to Sound and Ethnomusicological Documents, funded by the French Research Agency (ANR_ CONTINT 2012), involving IRIT_, CREM_, LAM_, LABRI_, LIMSI_, MNHN_, Parisson_
* TimeSide-DIADEMS_ : a set of Timeside plugins for hich level music analysis developed during the DIADEMS_ project
* SoundSoftware_ : Sustainable Software of Audio and Music Research
* DaCaRyH_ : Le rythme calypso à travers l’histoire : une approche en sciences des données (AHRC_ “Care for the Future” et le Labex-Passé_Présent_ "Les passés dans le présent")
* Kamoulox_ : Démixage en ligne de larges archives sonores (ANR_ Jeune Chercheur 2015)
* WASABI : Web Audio Semantic Aggregated in the Browser for Indexation (ANR_ 2016, currently being submitted)


.. _Telemeta: http://telemeta.org
.. _TimeSide: https://github.com/Parisson/TimeSide/
.. _OAI-PMH: http://fr.wikipedia.org/wiki/Open_Archives_Initiative_Protocol_for_Metadata_Harvesting
.. _Parisson: http://parisson.com
.. _CNRS: http://www.cnrs.fr
.. _MCC: http://www.culturecommunication.gouv.fr
.. _CREM: http://www.crem-cnrs.fr
.. _HumaNum: http://www.huma-num.fr
.. _IRIT: http://www.irit.fr
.. _LIMSI: http://www.limsi.fr/index.en.html
.. _LAM: http://www.lam.jussieu.fr
.. _LABRI: http://www.labri.fr
.. _MNHN: http://www.mnhn.fr
.. _MMSH: http://www.mmsh.univ-aix.fr
.. _UPMC: http://www.upmc.fr
.. _DIADEMS: http://www.irit.fr/recherches/SAMOVA/DIADEMS/fr/welcome/&cultureKey=en
.. _ANR: http://www.agence-nationale-recherche.fr/
.. _SABIOD: http://sabiod.telemeta.org
.. _CHANGELOG: http://github.com/Parisson/Telemeta/blob/master/CHANGELOG.rst
.. _Publications: https://github.com/Parisson/Telemeta-doc
.. _API : http://files.parisson.com/doc/telemeta/
.. _Player : https://github.com/Parisson/TimeSide/
.. _Example : http://archives.crem-cnrs.fr/archives/items/CNRSMH_E_2004_017_001_01/
.. _Homepage: http://telemeta.org
.. _GitHub: https://github.com/Parisson/Telemeta/
.. _IJLRDA: http://www.dalembert.upmc.fr/ijlrda/
.. _Labex-Passé_Présent: http://passes-present.eu/
.. _U-Paris10: http://www.u-paris10.fr/
.. _MdH: http://www.museedelhomme.fr/
.. _IRCAM: http://www.ircam.fr
.. _TimeSide-DIADEMS: https://github.com/ANR-DIADEMS/timeside-diadems
.. _DaCaRyH:  http://archives.crem-cnrs.fr/archives/fonds/CNRSMH_DACARYH/
.. _Kamoulox: http://www.agence-nationale-recherche.fr/?Projet=ANR-15-CE38-0003
.. _AHRC: http://www.ahrc.ac.uk/
.. _Queen Mary University: http://www.qmul.ac.uk/
.. _SoundSoftware : http://soundsoftware.ac.uk/
.. _C4DM: http://c4dm.eecs.qmul.ac.uk/
.. _CMAM: http://www.cmam.nat.tn/

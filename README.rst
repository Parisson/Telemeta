=============================
Telemeta: open web audio CMS
=============================

For personal or collaborative media archiving projects, research laboratories and digital humanities.

Based on Django, Python, HTML5, CSS and JavaScript.


Overview
=========

Telemeta is a free and open source web audio archiving software which introduces useful and secure methods to backup, index, transcode, analyse and publish any digitalized audio file with its metadata. It is dedicated to professionnals who wants to easily organize, backup and publish documented sound collections of audio files, CDs, digitalized vinyls and magnetic tapes over a strong database, in accordance with open web standards.

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
 * XML serialized backup
 * SQLite, MySQL, PostgreSQL or Oracle DB backends
 * Multi-language support (now english and french)
 * Video support (EXPERIMENTAL, WebM only)

This web audio CMS is exclusively based on open source modules and can be run on any Unix or Linux system.
It is mostly written in Python and JavaScript.


Installation, upgrade and usage
================================

See `INSTALL.rst <http://github.com/yomguy/Telemeta/blob/master/INSTALL.rst>`_ and `telemeta.org <http://telemeta.org>`_ for more informations.


News
======

1.4.4
+++++

 * no new fancy functions
 * full using of static files which are now in static/ (htdocs/ is now deprecated)
 * IMPORTANT : upgrade TimeSide to 0.4.1, add 'timeside' to INSTALLED_APPS and do: ./manage.py collectstatic
 * add various buttons, various bugfixes
 * after upgrading, always do: ./manage.py migrate

1.4.3
++++++

 * add solr-thumbnail for automatic thumbnail handling of all related media images (please install)
 * add static media handling for solr and all various telemeta public files
 * fix some wrong user properties
 * SECURITY: you need to move your TELEMETA_EXPORT_CACHE_DIR from TELEMETA_CACHE_DIR cache (see example/sandbox_sqlite/settings.py)
 * EXPERIMENTAL: WebM and MP4 video handling for items, NO transcode but decode, add a nice video.js player
 * RECOMMEND: install django-extensions
 * transitional package to 1.5 (maybe 1.4.4 *soon*)

1.4.2
++++++

 * add user revisions to user profile
 * move all edit buttons to main edit pages
 * new Format object and various enumerations
 * add last revision to item detail
 * various bugfixes

1.4.1
++++++

 Fix a bug for related media title parsing

1.4
++++++

For users:

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
 * before upgrading, you need to BACKUP and manually delete old wrong MediaCorpus and MediaCorpusRelated tables
 * we now use South for data model migration. Add 'south' to your apps and to do::

    ./manage.py syncdb
    ./manage.py migrate telemeta

See INSTALL.rst and email me if any pb!

Full changelog: see `CHANGELOG <http://github.com/yomguy/Telemeta/blob/master/CHANGELOG>`_


Demo
====

http://demo.telemeta.org

login: demo
password: demo


Original Examples
=================

`Sound archives of the French Ethnomusicology Research Center (CREM) and the Musée de l'Homme <http://archives.crem-cnrs.fr>`_ :

 * a 100 year old world database migrated,
 * more than 5000 geolocated collections,
 * more than 32000 geolocated items,
 * more than 11000 sounds included
 * 700 Go of original ethnological music files accessible through the web.

`Sound archives of the team "Lutherie, Acoustique et Musique" (LAM) of the IJLRDA institute - University Pierre et Marie Curie (Paris 6) <http://telemeta.lam.jussieu.fr>`_ :

 * various musical instruments recorded for research purposes
 * started in sept. 2012

`Sound archives Parisson <http://parisson.telemeta.org>`_ :

 * various electronic sounds and original electronic music produced by Parisson


Bugs and feedback
=================

You are welcome to freely use this application in accordance with its licence.
If you find some bugs, PLEASE leave a ticket on this page:

http://telemeta.org/newticket

You can also leave a ticket to request some new interesting features for the next versions.
And even if Telemeta suits you, please give us some feedback !


Related projects
================

`TimeSide <http://code.google.com/p/timeside/>`_ - open and fast web audio components

    a python library to compute audio analysis, transcode, and streaming to browsers.


Contact
=======

Homepage: http://telemeta.org

E-mails:

 * Guillaume Pellerin <yomguy@parisson.com>,
 * Olivier Guilyardi <olivier@samalyse.com>,
 * Riccardo Zaccarelli <riccardo.zaccarelli@gmail.com>

Twitter:

 * http://twitter.com/telemeta
 * http://twitter.com/parisson_studio
 * http://twitter.com/yomguy

Development
===========

You are welcome to participate to the development of the Telemeta project.
The official project site is `telemeta.org <http://telemeta.org>`_ but you can find a mirror on `GitHub <https://github.com/yomguy/Telemeta>`_.

To get the lastest development version, you need Git and run::

    $ git clone http://vcs.parisson.com/git/telemeta.git

or::

    $ git clone git://github.com/yomguy/Telemeta.git


License
=======

CeCILL v2, compatible with GPL v2 (see `LICENSE <http://github.com/yomguy/Telemeta/blob/master/LICENSE>`_)


Sponsors
========

The Telemeta project is developed by Parisson. It is sponsored by :

  * CNRS : Centre National de la Recherche Scientifique (the french Natianal Research and Scientific Center)
    http://cnrs.fr
  * CREM : Centre de Recherche en Ethnomusicology (the french Ethnomusicology Research Center)
    http://www.crem-cnrs.fr
  * LAM : Equipe Lutherie, Acoustique et Musique de l'Université Pierre et Marie Curie de Paris
    (Instrument design, Acoustic and Music team of the Pierre & Marie Curie University)
    http://www.lam.jussieu.fr/
  * MuCEM : Musée des Civilisations de l'Europe et de la Méditerranée
    http://www.musee-europemediterranee.org
  * MMSH : Maison Méditerranéenne des Sciences de l'Homme
    http://www.mmsh.univ-aix.fr/


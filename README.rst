=============================
Telemeta: open web audio CMS
=============================

Introduction
============

Telemeta is a free and open source web audio archiving software which introduces useful and secure methods to backup, index, transcode, analyse and publish any digitalized audio file with its metadata. It is dedicated to professionnals who wants to easily organize, backup and publish documented sound collections of audio files, CDs, digitalized vinyls and magnetic tapes over a strong database, in accordance with open web standards.

Here are the main features of Telemeta:

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
 * Strong SQL or Oracle backend
 * Multi-language support (now english and french)

This web audio CMS is exclusively based on open source modules and can be run on any Unix or Linux system. It is mostly written in Python and JavaScript.


Installation, upgrade and usage
================================

See `INSTALL.rst <http://github.com/yomguy/Telemeta/blob/master/INSTALL.rst>`_ and `telemeta.org <http://telemeta.org>`_ for more informations.


News
======

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

See INSTALL.rst and email me if any pb! (you may, for example, not use 0002 migration)

Full changelog : see `CHANGELOG <http://github.com/yomguy/Telemeta/blob/master/CHANGELOG>`_


Development
===========

To participate to the development of telemeta, you will need a login/password couple.
You're welcome to email us to join and commit your great ideas ;)

To get the lastest development version, you need subversion and run::

    $ git clone http://vcs.parisson.com/git/telemeta.git

Licence
=======

CeCILL v2 (see LICENSE)


Bugs and feedback
=================

You are welcome to freely use this application in accordance with its licence.
If you find some bugs, PLEASE leave a ticket on this page:

http://telemeta.org/newticket

You can also leave a ticket to request some new interesting features for the next versions.
And even if Telemeta suits you, please give us some feedback !


Related projects
================

TimeSide (Web Audio Components): http://code.google.com/p/timeside/


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

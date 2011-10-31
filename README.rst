=======
README
=======

Telemeta: a web Audio Content Management System

Introduction
============

Telemeta is a web audio archiving program which introduces useful and secure methods to backup, index, transcode, analyse and publish any digitalized audio file with its metadata. It is dedicated to professionnals who wants to easily organize, backup and publish documented sound collections of audio files, CDs, digitalized vinyls and magnetic tapes over a strong database, in accordance with open web standards.

Here are the main features of Telemeta:

    * Secure archiving, editing and publishing of audio files over internet.
    * User friendly web frontend including workflows and high level search methods
    * Smart dynamical and skinnable audio player (thanks to Timeside and SoundManager2)
    * "On the fly" analyzing, transcoding and metadata embedding based on an easy plugin architecture
    * Multi-format support : FLAC, OGG, MP3, WAV and more
    * GEO Navigator for audio geolocalization
    * DublinCore compatibility
    * OAI-PMH data provider
    * XML serialized backup
    * Strong SQL backend

The Telemeta data model is based on 'collections' and 'items'. A collection is described
by its metadata and includes original audio items (sounds) and its own metadata. This
existing model has been designed to fit the one of the French Centre of Etnomusicology (CREM)
but could be easily adapted/overrided to sue other data structures.


Installation, upgrade and usage
================================

**WARNING** : sorry the setup process of 1.1 was just wrong, please upgrade to 1.2 !

See `INSTALL.rst <http://telemeta.org/browser/INSTALL.rst>`_ and `telemeta.org <http://telemeta.org>`_ for more informations.


Changelog
=========

See `CHANGELOG <http://telemeta.org/browser/CHANGELOG>`_


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

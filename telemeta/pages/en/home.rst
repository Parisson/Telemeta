===================================================
Telemeta : Web Audio Content Management System
===================================================

`Telemeta <http://telemeta.org>`_ is an open source web audio archiving program which introduces useful and secure methods to backup, index, transcode, analyse and publish any digitalized audio file with its metadata. It is dedicated to professionnals who wants to easily backup and publish documented sounds from collections of LP and EP vinyls, magnetic tapes or audio CDs over a strong database, in accordance with open standards.

Key features of Telemeta:
    
 * Secure archiving, editing and publishing of audio files over internet.
 * User friendly web frontend including workflows and high level search methods
 * Smart dynamical and skinnable audio player (thanks to `TimeSide <http://code.google.com/p/timeside/> and `SoundManager2 <http://www.schillmania.com/projects/soundmanager2/>`_)
 * "On the fly" analyzing, transcoding and metadata embedding based on an easy plugin architecture
 * Temporal and collaborative indexation with fast user marker management
 * Multi-format support : FLAC, OGG, MP3, WAV and more
 * User management with individual profiles and rights
 * Playlist management for users with CSV data export
 * Geo-Navigator for audio geolocalization
 * `DublinCore <http://dublincore.org/>`_ compatibility
 * `OAI-PMH <http://www.openarchives.org/pmh/>`_ data provider
 * RSS feeds generator
 * XML serialized backup
 * Strong SQL or Oracle backend

The Telemeta data model is now based on *collection* and *item* elements. A *collection* is described by its metadata and is related to audio *items*. An *item* embeds audio files with its metadata. This model has been designed to fit the one of the French Centre of Ethnomusicology (`CREM <http://www.crem-cnrs.fr>`_) of the University of Paris Ouest - Nanterre but could be easily adapted or overrided to suit other data structures.

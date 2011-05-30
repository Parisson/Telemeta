# -*- coding: utf-8 -*-
from distutils.core import setup
from distutils.command.install import INSTALL_SCHEMES
import os
import sys

def fullsplit(path, result=None):
    """
    Split a pathname into components (the opposite of os.path.join) in a
    platform-neutral way.
    """
    if result is None:
        result = []
    head, tail = os.path.split(path)
    if head == '':
        return [tail] + result
    if head == path:
        return result
    return fullsplit(head, [tail] + result)

# Tell distutils to put the data_files in platform-specific installation
# locations. See here for an explanation:
# http://groups.google.com/group/comp.lang.python/browse_thread/thread/35ec7b2fed36eaec/2105ee4d9e8042cb
for scheme in INSTALL_SCHEMES.values():
    scheme['data'] = scheme['purelib']

# Compile the list of packages available, because distutils doesn't have
# an easy way to do this.
packages, data_files = [], []
root_dir = os.path.dirname(__file__)
if root_dir != '':
    os.chdir(root_dir)
telemeta_dir = 'telemeta'

for dirpath, dirnames, filenames in os.walk(telemeta_dir):
    # Ignore dirnames that start with '.'
    for i, dirname in enumerate(dirnames):
        if dirname.startswith('.'): del dirnames[i]
    if '__init__.py' in filenames:
        packages.append('.'.join(fullsplit(dirpath)))
    elif filenames:
        data_files.append([dirpath, [os.path.join(dirpath, f) for f in filenames]])

# Dynamically calculate the version based on telemeta.VERSION.
version = __import__('telemeta').__version__

setup(
  name = "Telemeta",
  url = "http://telemeta.org",
  description = "Web Audio Content Management System",
  author = ["Guillaume Pellerin, Olivier Guilyardi", "Riccardo Zaccarelli"],
  author_email = ["yomguy@parisson.com","olivier@samalyse.com", "riccardo.zaccarelli@gmail.com"],
  version = version,
  packages = packages,
  data_files = data_files,
  intall_requires = ['timeside'],
  classifiers = ['Environment :: Web Environment', 'Framework :: Django', 'Intended Audience :: Science/Research', 'Intended Audience :: Education', 'Programming Language :: Python', 'Programming Language :: JavaScript', 'Topic :: Internet :: WWW/HTTP :: Dynamic Content', 'Topic :: Internet :: WWW/HTTP :: WSGI :: Application', 'Topic :: Multimedia :: Sound/Audio', 'Topic :: Multimedia :: Sound/Audio :: Analysis', 'Topic :: Multimedia :: Sound/Audio :: Players', 'Topic :: Scientific/Engineering :: Information Analysis', 'Topic :: System :: Archiving',  ], 
  long_description = """
Telemeta is a web audio archiving program which introduces useful and secure methods to backup, index, transcode, analyse and publish any digitalized audio file with its metadata. It is dedicated to professionnals who wants to easily backup and publish documented sounds from collections of vinyls, magnetic tapes or audio CDs over a strong database, in accordance with open standards.

Here are the main features of Telemeta:

 * Secure archiving, editing and publishing of audio files over internet.
 * User friendly web frontend including workflows and high level search methods
 * Smart dynamical and skinnable audio player (thanks to TimeSide and SoundManager2)
 * "On the fly" analyzing, transcoding and metadata embedding based on an easy plugin architecture
 * Temporal and collaborative indexation with fast user marker management
 * Multi-format support : FLAC, OGG, MP3, WAV and more
 * User management with individual profiles and rights
 * Playlist management for users with CSV data export
 * Geo-Navigator for audio geolocalization
 * DublinCore compatibility
 * OAI-PMH data provider
 * RSS feeds generator
 * XML serialized backup
 * Strong SQL or Oracle backend

The Telemeta data model is now based on *collection* and *item* elements. 
A *collection* is described by its metadata and is related to audio *items*. 
An *item* embeds audio files with its metadata. 
This model has been designed to fit the one of the French Centre of Ethnomusicology 
(`CREM <http://www.crem-cnrs.fr>`_) of the University of Paris Ouest - Nanterre 
but could be easily adapted or overrided to suit other data structures.

See http://telemeta.org for more informations.
"""
)

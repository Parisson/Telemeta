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
  name = "telemeta",
  url = "/http://svn.parisson.org/telemeta",
  description = "web frontend to backup, transcode and tag any audio content with metadata",
  author = ["Guillaume Pellerin, Olivier Guilyardi"],
  author_email = ["pellerin@parisson.com","olivier@samalyse.com"],
  version = version,
  packages = packages,
  data_files = data_files,
  long_description = """
Telemeta is a web audio archiving program which introduces useful and secure methods to
backup, index, transcode, analyse and publish any digitalized audio file with its metadata.
It is dedicated to professionnals who wants to easily backup and publish documented sounds
from collections of vinyls, magnetic tapes or audio CDs over a strong database, in accordance
with open standards.

Here are the main features of Telemeta:

    * Secure archiving, editing and publishing of audio files over internet.
    * "On the fly" transcoding and metadata encapsulating (FLAC, OGG, MP3, WAV, etc..)
    * User friendly web frontend including workflows and high level search methods
    * Smart dynamical and skinnable audio player (thanks to Timeside and soundmanager2)
    * "On the fly" complex audio analyzers based on an easy plugin architecture
    * Strong SQL backend
    * XML metadata backup
    * Auto audio-marking with synthetized voices reading metadata (optional)
    * Anti-corruption data security management with par2 recovery keys
    * Data synchronizing over remote servers (rsync + ssh methods)

The Telemeta data model is based on 'collections' and 'items'. A collection is described
by its metadata and includes original audio items (sounds) and its own metadata. This
existing model has been designed to fit the one of the French Centre of Etnomusicology (CREM)
but could be easily adapted/overrided to sue other data structures.

See http://telemeta.org for more informations.
"""
)

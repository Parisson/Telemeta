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
version_tuple = __import__('telemeta').__version__
if version_tuple[2] is not None:
    version = "%d.%d_%s" % version_tuple
else:
    version = "%d.%d" % version_tuple[:2]

setup(
  name = "telemeta",
  url = "/http://svn.parisson.org/telemeta",
  description = "web frontend to backup, transcode and tag any audio content with metadata",
  author = ["Guillaume Pellerin, Olivier Guilyardi"],
  author_email = ["pellerin@parisson.com"],
  version = "0.3.1",
  packages = packages,
  data_files = data_files,
  long_description = """
Telemeta is a global audio archiving program which introduces useful and secure
indexing methods to backup digitalized audio files and metadata dictionnaries.
It is dedicated to backup any digitized and documented sound from collections of
vinyls, magnetic tapes or audio CD over a strong database in accordance with
many standards. Export functions also encapsulate edited metadata into
compressed file. The object style architecture will soon provide user-friendly
interfaces and plugin' style audio processing.

Here are the main features of Telemeta: 

    * Secure media editing and archiving over networks
    * Easy transcoding
    * Full tagging and marking methods
    * XML metadata backup
    * Web interface introducing WorkFlow
    * SQL backend
    * Data anti-corruption security with par2 recovery keys
    * Data synchronizing over remote servers (rsync)
    * Auto AudioMarking from metadata (thanks to Festival and Ecasound)

The Telemeta concept is based on collections. A collection includes original
sounds - or albums containing sounds - which will be backuped in a secure way
with a view of transcoded 'public' formats (WAV, FLAC, MP3, OGG and many more
soon...) including metadata editing and publishing tools.

See http://svn.parisson.org/telemeta/ for more informations.
"""
)


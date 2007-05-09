# Copyright (C) 2007 Samalyse SARL
# All rights reserved.
#
# This software is licensed as described in the file COPYING, which
# you should have received as part of this distribution. The terms
# are also available at http://svn.parisson.org/telemeta/TelemetaLicense.
#
# Author: Olivier Guilyardi <olivier@samalyse.com>

from telemeta.core import *

class IMediaItemVisualizer(Interface):
    """Media item visualizer driver interface"""

    def get_id():
        """Return a short id alphanumeric, lower-case string."""

    def get_name():
        """Return the visualization name, such as "Waveform", "Spectral view", 
        etc.. 
        """
    
    def render(media_item, options=None):
        """Generator that streams the visualization output as a PNG image"""
            

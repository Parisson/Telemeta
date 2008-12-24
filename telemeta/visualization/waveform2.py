# Copyright (C) 2007 Samalyse SARL
# All rights reserved.
#
# This software is licensed as described in the file COPYING, which
# you should have received as part of this distribution. The terms
# are also available at http://svn.parisson.org/telemeta/TelemetaLicense.
#
# Authors: Olivier Guilyardi <olivier@samalyse.com>
#          Guillaume Pellerin <pellerin@parisson.com>

from telemeta.core import *
from telemeta.visualization.api import IMediaItemVisualizer
from telemeta.visualization.octave_core import OctaveCoreVisualizer

class WaveformVisualizer2(OctaveCoreVisualizer):
    """Octave temporal view visualization driver"""
    
    implements(IMediaItemVisualizer)

    def __init__(self):
        self.set_m_file('waveform2img.m')
        self.buffer_size = 0xFFFF
        self.trans_type = 'png'
        
    def get_id(self):
        return "waveform2"

    def get_name(self):
        return "Waveform (octave)"
    
    def set_colors(self, background=None, scheme=None):
        pass

    def render(self, media_item, options=None):
        """Generator that streams the temporal view as a PNG image"""

        stream = self.octave_to_png_stream(media_item)
        return stream
        

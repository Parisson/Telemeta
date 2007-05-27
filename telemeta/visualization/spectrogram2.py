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

class SpectrogramVisualizer2(OctaveCoreVisualizer):
    """Octave spectral view visualization driver"""
    
    implements(IMediaItemVisualizer)

    def __init__(self):
        self.set_m_file('spectrogram2img.m')
        self.buffer_size = 0xFFFF
        self.trans_type = 'ppm'
        
    def get_id(self):
        return "spectrogram2"

    def get_name(self):
        return "Spectrogram2 (< 300s)"
    
    def render(self, media_item, options=None):
        """Generator that streams the spectral view as a PNG image"""

        stream = self.octave_to_png_stream(media_item)
        return stream
        

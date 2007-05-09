# Copyright (C) 2007 Samalyse SARL
# All rights reserved.
#
# This software is licensed as described in the file COPYING, which
# you should have received as part of this distribution. The terms
# are also available at http://svn.parisson.org/telemeta/TelemetaLicense.
#
# Author: Olivier Guilyardi <olivier@samalyse.com>

from telemeta.core import *
from telemeta.visualization.api import IMediaItemVisualizer
from telemeta.visualization.snack_core import SnackCoreVisualizer

class SpectrogramVisualizer(SnackCoreVisualizer):
    """Spectral view visualization driver"""

    implements(IMediaItemVisualizer)

    # possible alternative:
    # http://jokosher.python-hosting.com/file/jokosher-extra/Waveform.py

    def get_id(self):
        return "spectrogram"

    def get_name(self):
        return "Spectrogram"
    
    def render(self, media_item, options=None):
        """Generator that streams the spectral view as a PNG image"""

        canvas = self.get_snack_canvas()
        snd = self.get_snack_sound(media_item)

        canvas.create_spectrogram(0, 10, sound=snd, height=180, width=300 ,
            windowtype="hamming", fftlength=1024, topfrequency=5000, channel="all", winlength=64)


        stream = self.canvas_to_png_stream(canvas)

        return stream
        




        

            

# Copyright (C) 2008 Parisson SARL
# All rights reserved.
#
# This software is licensed as described in the file COPYING, which
# you should have received as part of this distribution. The terms
# are also available at http://svn.parisson.org/telemeta/TelemetaLicense.
#
# Author: Guillaume Pellerin <pellerin@parisson.com>

from telemeta.core import *
from telemeta.visualization.api import IMediaItemVisualizer
from django.conf import settings
from tempfile import NamedTemporaryFile
from telemeta.visualization.wav2png import *

class WaveFormVisualizer(Component):
    """WaveForm visualization driver (python style)"""

    implements(IMediaItemVisualizer)

    def get_id(self):
        return "waveform3"

    def get_name(self):
        return "Waveform (audiolab)"
    
    def render(self, media_item, options=None):
        """Generator that streams the waveform as a PNG image with a python method"""

        wav_file = settings.MEDIA_ROOT + '/' + media_item.file
        pngFile_w = NamedTemporaryFile(suffix='.png')
        pngFile_s = NamedTemporaryFile(suffix='.png')
        image_width = 305
        image_height = 150
        fft_size = 2048
        args = (wav_file, pngFile_w.name, pngFile_s.name, image_width, image_height, fft_size)
        create_png(*args)

        buffer = pngFile_w.read(0xFFFF)
        while buffer:
            yield buffer
            buffer = pngFile_w.read(0xFFFF)

        pngFile_w.close()
        pngFile_s.close()


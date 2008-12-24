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
from django.conf import settings
from tempfile import NamedTemporaryFile
import os
import os.path

class WaveFormVisualizer(Component):
    """WaveForm visualization driver"""

    implements(IMediaItemVisualizer)

    # possible alternative:
    # http://jokosher.python-hosting.com/file/jokosher-extra/Waveform.py

    def get_id(self):
        return "waveform"

    def get_name(self):
        return "Waveform"
    
    def set_colors(self, background=None, scheme=None):
        pass

    def render(self, media_item, options=None):
        """Generator that streams the waveform as a PNG image"""

        pngFile = NamedTemporaryFile(suffix='.png')
        wav2png = os.path.dirname(__file__) + '/wav2png/wav2png'
        args  = "-i " + media_item.file.path + " "
        args += "-o " + pngFile.name + " "
        args += "-b ffffff "
        args += "-l 000088 "
        args += "-z 990000 "
        args += "-w 300 "
        args += "-h 151 "
       
        os.system(wav2png + " " + args)

        buffer = pngFile.read(0xFFFF)
        while buffer:
            yield buffer
            buffer = pngFile.read(0xFFFF)

        pngFile.close()            


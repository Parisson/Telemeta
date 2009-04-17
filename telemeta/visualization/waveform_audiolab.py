# -*- coding: utf-8 -*-
# Copyright (C) 2008 Parisson SARL
# All rights reserved.
#
# This software is a computer program whose purpose is to backup, analyse,
# transcode and stream any audio content with its metadata over a web frontend.

# This software is governed by the CeCILL  license under French law and
# abiding by the rules of distribution of free software.  You can  use,
# modify and/ or redistribute the software under the terms of the CeCILL
# license as circulated by CEA, CNRS and INRIA at the following URL
# "http://www.cecill.info".

# As a counterpart to the access to the source code and  rights to copy,
# modify and redistribute granted by the license, users are provided only
# with a limited warranty  and the software's author,  the holder of the
# economic rights,  and the successive licensors  have only  limited
# liability.

# In this respect, the user's attention is drawn to the risks associated
# with loading,  using,  modifying and/or developing or reproducing the
# software by the user in light of its specific status of free software,
# that may mean  that it is complicated to manipulate,  and  that  also
# therefore means  that it is reserved for developers  and  experienced
# professionals having in-depth computer knowledge. Users are therefore
# encouraged to load and test the software's suitability as regards their
# requirements in conditions enabling the security of their systems and/or
# data to be ensured and,  more generally, to use and operate it in the
# same conditions as regards security.

# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL license and that you accept its terms.
#
# Author: Guillaume Pellerin <pellerin@parisson.com>

from telemeta.core import *
from telemeta.visualization.api import IMediaItemVisualizer
from django.conf import settings
from tempfile import NamedTemporaryFile
from telemeta.visualization.wav2png import *

class WaveFormVisualizerAudiolab(Component):
    """WaveForm visualization driver (python style thanks to wav2png.py and scikits.audiolab)"""

    implements(IMediaItemVisualizer)

    bg_color = None
    color_scheme = None

    def get_id(self):
        return "waveform_audiolab"

    def get_name(self):
        return "Waveform (audiolab)"

    def set_colors(self, background=None, scheme=None):
        self.bg_color = background
        self.color_scheme = scheme

    def render(self, media_item, width=None, height=None, options=None):
        """Generator that streams the waveform as a PNG image with a python method"""

        wav_file = media_item.file.path
        pngFile = NamedTemporaryFile(suffix='.png')

        if not width == None:
            image_width = width
        else:
            image_width = 1500
        if not height == None:
            image_height = height
        else:
            image_height = 200

        fft_size = 2048
        args = (wav_file, pngFile.name, image_width, image_height, fft_size, 
                self.bg_color, self.color_scheme)
        create_wavform_png(*args)

        buffer = pngFile.read(0xFFFF)
        while buffer:
            yield buffer
            buffer = pngFile.read(0xFFFF)

        pngFile.close()


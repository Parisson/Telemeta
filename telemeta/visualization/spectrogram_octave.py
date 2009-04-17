# -*- coding: utf-8 -*-
# Copyright (C) 2007 Samalyse SARL
# Copyright (c) 2007-2009 Guillaume Pellerin <yomguy@parisson.com>
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
# Authors: Olivier Guilyardi <olivier@samalyse.com>
#          Guillaume Pellerin <pellerin@parisson.com>

from telemeta.core import *
from telemeta.visualization.api import IMediaItemVisualizer
from telemeta.visualization.octave_core import OctaveCoreVisualizer

class SpectrogramVisualizerOctave(OctaveCoreVisualizer):
    """Octave spectral view visualization driver"""
    
    implements(IMediaItemVisualizer)

    def __init__(self):
        self.set_m_file('spectrogram2img.m')
        
    def get_id(self):
        return "spectrogram_octave"

    def get_name(self):
        return "Spectrogram (octave)"

    def set_colors(self, background=None, scheme=None):
        pass
    
    def render(self, media_item, width=None, height=None, options=None):
        """Generator that streams the spectral view as a PNG image"""

        stream = self.octave_to_png_stream(media_item)
        for chunk in stream:
            yield chunk


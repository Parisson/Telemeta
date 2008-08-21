# Copyright (C) 2008 Parisson SARL
# All rights reserved.
#
# This software is licensed as described in the file COPYING, which
# you should have received as part of this distribution. The terms
# are also available at http://svn.parisson.org/telemeta/TelemetaLicense.
#
# Author: Guillaume Pellerin <yomguy@parisson.com>

from telemeta.analysis.core import *
from telemeta.analysis.api import IMediaItemAnalyzer
import numpy

class MaxLevelAnalyzer(AudioProcessor):
    """Media item analyzer driver interface"""

    implements(IMediaItemAnalyzer)

    def __init__(self):
        self.fft_size = 2048
        self.window_function = numpy.hanning
        self.window = self.window_function(self.fft_size)
        
    def get_id(self):
        return "max_level"

    def get_name(self):
        return "Maximum level"

    def get_unit(self):
        return "dB"

    def render(self, media_item, options=None):
        self.pre_process(media_item)
        samples = self.get_mono_samples()
        print str(numpy.max(samples))
        return numpy.round(20*numpy.log10(numpy.max(samples)),2)
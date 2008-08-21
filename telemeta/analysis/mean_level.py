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

class MeanLevelAnalyser(AudioProcessor):
    """Media item analyzer driver interface"""

    implements(IMediaItemAnalyzer)

    def __init__(self):
        self.fft_size = 2048
        self.window_function = numpy.hanning
        self.window = self.window_function(self.fft_size)
        
    def get_id(self):
        return "mean_level"

    def get_name(self):
        return "Mean level"

    def get_unit(self):
        return "dB"

    def render(self, media_item, options=None):
        self.pre_process(media_item)
        samples = self.get_mono_samples()
        size = numpy.size(samples)
        return numpy.round(20*numpy.log10(numpy.mean(numpy.sqrt(numpy.square(samples)))),2)

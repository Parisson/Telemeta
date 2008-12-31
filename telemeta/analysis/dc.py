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

class MeanDCShiftAnalyser(AudioProcessor):
    """Media item analyzer driver interface"""

    implements(IMediaItemAnalyzer)

    def get_id(self):
        return "dc"

    def get_name(self):
        return "Mean DC shift"

    def get_unit(self):
        return "%"

    def render(self, media_item, options=None):
        self.pre_process(media_item)
        samples = self.get_mono_samples()
        return numpy.round(100*numpy.mean(samples),4)

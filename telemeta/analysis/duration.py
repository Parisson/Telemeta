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
import datetime

class DurationAnalyzer(AudioProcessor):
    """Media item analyzer driver interface"""

    implements(IMediaItemAnalyzer)

    def get_id(self):
        return "duration"

    def get_name(self):
        return "Duration"

    def get_unit(self):
        return "h:m:s"

    def render(self, media_item, options=None):
        self.pre_process(media_item)
        media_time = numpy.round(float(self.frames)/(float(self.samplerate)*float(self.channels)),0)
        return datetime.timedelta(0,media_time)

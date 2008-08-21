# Copyright (C) 2008 Parisson SARL
# All rights reserved.
#
# This software is licensed as described in the file COPYING, which
# you should have received as part of this distribution. The terms
# are also available at http://svn.parisson.org/telemeta/TelemetaLicense.
#
# Author: Guillaume Pellerin <yomguy@parisson.com>

from telemeta.core import *

class IMediaItemAnalyzer(Interface):
    """Media item analyzer driver interface"""

    def get_id():
        """Return a short id alphanumeric, lower-case string."""

    def get_name():
        """Return the analysis name, such as "Mean Level", "Max level",
        "Total length, etc..
        """

    def get_unit():
        """Return the unit of the data such as "dB", "seconds", etc...
        """
    
    def render(media_item, options=None):
        """Return a list containing data results of the process"""
            

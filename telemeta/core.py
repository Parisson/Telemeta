# -*- coding: utf-8 -*-
#
# Copyright (C) 2007 Samalyse SARL
# All rights reserved.
#
# This software is licensed as described in the file COPYING, which
# you should have received as part of this distribution. 
#
# Author: Olivier Guilyardi <olivier@samalyse.com>

__all__ = ['TelemetaError']


class TelemetaError(Exception):
    """Exception base class for errors in Telemeta."""
    # FIXME: is this redundant with Django's error handling ?

#    def __init__(self, message, title=None, show_traceback=False):
#        Exception.__init__(self, message)
#        self.message = message
#        self.title = title
#        self.show_traceback = show_traceback


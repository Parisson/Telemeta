# -*- coding: utf-8 -*-
#
# Copyright (C) 2007 Samalyse SARL
# Copyright (C) 2003-2005 Edgewall Software
# Copyright (C) 2003-2004 Jonas Borgström <jonas@edgewall.com>
# Copyright (C) 2004-2005 Christopher Lenz <cmlenz@gmx.de>
# All rights reserved.
#
# This software is licensed as described in the file COPYING, which
# you should have received as part of this distribution.
#
# Author: Jonas Borgström <jonas@edgewall.com>
#         Christopher Lenz <cmlenz@gmx.de>
#         Olivier Guilyardi <olivier@samalyse.com>

__all__ = ['TelemetaError']


class TelemetaError(Exception):
    """Exception base class for errors in Telemeta."""
    pass


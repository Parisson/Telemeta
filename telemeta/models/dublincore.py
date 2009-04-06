# Copyright (C) 2007 Samalyse SARL
# All rights reserved.
#
# This software is licensed as described in the file COPYING, which
# you should have received as part of this distribution. The terms
# are also available at http://svn.parisson.org/telemeta/TelemetaLicense.
#
# Author: Olivier Guilyardi <olivier@samalyse.com>

class Resource(object):
    "Represent a Dublin Core resource"

    elements = []

    def __init__(self, *args):
        self.elements = args  

    def flatten(self):
        """Convert the resource to a dictionary with element names as keys.

        Warnings: 
        - refinements are lost during this conversion,
        - if there are several occurences of the same element, only the first is 
        used, others are lost.
        - all values are converted to strings
        """
        result = {}
        for element in self.elements:
            if not result.has_key(element.name):
                result[element.name] = unicode(element.value)
        return result

    def to_list(self):
        """Convert the resource to unqualified dublin core, as a list of the form:
           [(key, value), ...]"""
        result = []
        for element in self.elements:
            result.append((element.name, unicode(element.value)))
        return result

class Element(object):
    "Represent a Dublin Core element"

    def __init__(self, name, field=None, value=None, refinement=None):
        self.name = name
        self.value = value
        self.refinement = refinement
        self.field = field
        

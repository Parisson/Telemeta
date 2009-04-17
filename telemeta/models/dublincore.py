# -*- coding: utf-8 -*-
# Copyright (C) 2007 Samalyse SARL

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
        

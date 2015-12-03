# -*- coding: utf-8 -*-
#
# Copyright (C) 2010 jdunck
# Copyright (C) 2011 Parisson

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
# Author: jdunck
# taken from https://github.com/jdunck/python-unicodecsv.git

import csv, codecs, cStringIO

def _stringify(s, encoding):
    if type(s)==unicode:
        return s.encode(encoding)
    elif isinstance(s, (int , float)):
        pass #let csv.QUOTE_NONNUMERIC do its thing.
    elif type(s) != str:
        s=str(s)
    return s

def _stringify_list(l, encoding):
    return [_stringify(s, encoding) for s in l]


class StreamCSVException(Exception):
    pass


class UnicodeCSVWriter(object):
    def __init__(self, f, elements, dialect=csv.excel, encoding="utf-8", **kwds):
        self.dialect = dialect
        self.encoding = encoding
        self.writer = csv.writer(f, dialect=dialect, **kwds)
        self.line = 0
        self.elements = elements
        self.tags = []
        self.get_tags(self.elements[0])

    def get_tags(self, element):
        _dict = element.to_dict_with_more()

        for key in _dict.keys():
            if not key in self.tags:
                self.tags.append(key)

        # code and title on the two first column
        self.tags.remove('code')
        self.tags.remove('title')
        self.tags.sort()
        self.tags.insert(0, 'title')
        self.tags.insert(0, 'code')

    def output(self):
        yield self.writer.writerow(self.tags)
        for element in self.elements:
            yield self.writer.writerow(_stringify_list(element.to_row(), self.encoding))


class Echo(object):
    """An object that implements just the write method of the file-like
    interface.
    """
    def write(self, value):
        """Write the value by returning it, instead of storing in a buffer."""
        return value

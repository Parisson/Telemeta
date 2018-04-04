# -*- coding: utf-8 -*-
#
# Copyright (C) 2010 jdunck
# Copyright (C) 2011 Parisson

# This file is part of Telemeta.

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
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


class UnicodeCSVWriter(object):
    def __init__(self, f, elements, dialect=csv.excel, encoding="utf-8", **kwds):
        self.dialect = dialect
        self.encoding = encoding
        self.writer = csv.writer(f, dialect=dialect, **kwds)
        self.line = 0
        self.elements = elements
        self.tags = []
        if self.elements:
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
            yield self.writer.writerow(_stringify_list(element.to_row(self.tags), self.encoding))


class Echo(object):
    """An object that implements just the write method of the file-like
    interface.
    """
    def write(self, value):
        """Write the value by returning it, instead of storing in a buffer."""
        return value

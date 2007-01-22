#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Author: Ingelrest François (Athropos@gmail.com)
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Library General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301 USA

# Supported types
# 'bool' type must be placed *before* 'int' type, otherwise booleans are detected as integers
types = {bool : 'bool', int : 'int', str : 'str'}

# Return a String with the type of value
def getType(value) :
    for type in types.keys() :
        if isinstance(value, type) :
            return types[type]
    raise TypeError, str(value) + ' has an unsupported type'

# Return value, casted into type
def cast(value, type) :
    if type == 'bool' :
        if value == 'True' :
            return True
        return False
    elif type == 'int' :
        return int(value)
    elif type == 'str' :
        return str(value)
    raise TypeError, type + ' is an unsupported type'

# -*- coding: utf-8 -*-
# Copyright (C) 2007-2010 Samalyse SARL

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
# Authors: Olivier Guilyardi <olivier@samalyse.com>

from django.test import TestCase
from telemeta.util.unaccent import unaccent_icmp

class UnaccentTestCase(TestCase):
    def testSorting(self):
        strings = [u'Métro', u'évasion', u'àccent', u'È', u'île', u'arrivée', u'elle']
        strings.sort(unaccent_icmp)
        expected = [u'àccent', u'arrivée', u'È', u'elle', u'évasion', u'île', u'Métro']
        self.assertEquals(strings, expected)


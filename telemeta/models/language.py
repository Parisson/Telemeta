# -*- coding: utf-8 -*-
# Copyright (C) 2011-2012 Parisson SARL

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
# Authors:
#          Guillaume Pellerin <yomguy@parisson.com>

from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from telemeta.models.core import *

SCOPE_CHOICES = (('I', 'Individual'), ('M', 'Macrolanguage'), ('S', 'Special'))

TYPE_CHOICES = (('A', 'Ancient'), ('C', 'Constructed'), ('E', 'Extinct'),
                ('H', 'Historical'), ('L', 'Living'), ('S', 'Special'))

class Language(ModelCore):
    "ISO 639-3 normalized languages"

    identifier      = CharField(_('identifier'), max_length=3)
    part2B          = CharField(_('equivalent ISO 639-2 identifier (bibliographic)'), max_length=3)
    part2T          = CharField(_('equivalent ISO 639-2 identifier (terminologic)'), max_length=3)
    part1           = CharField(_('equivalent ISO 639-1 identifier'), max_length=1)
    scope           = CharField(_('scope'), choices=SCOPE_CHOICES, max_length=1)
    type            = CharField(_('type'), choices=TYPE_CHOICES, max_length=1)
    name            = CharField(_('name'))
    comment         = TextField(_('comment'))

    def __str__(self):
        return self.name.encode('utf-8')

    class Meta(MetaCore):
        db_table = 'languages'
        ordering = ['name']
        verbose_name_plural = _('languages')

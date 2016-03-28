# -*- coding: utf-8 -*-
# Copyright (C) 2010 Samalyse SARL
# Copyright (C) 2010-2014 Parisson SARL

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
#          David LIPSZYC <davidlipszyc@gmail.com>
#          Guillaume Pellerin <yomguy@parisson.com>


from telemeta.models.core import *
from telemeta.models.fields import *
from django.utils.translation import ugettext_lazy as _


class Identifier(ModelCore):
    """Resource identifier"""

    identifier = CharField(_('identifier'), max_length=255, blank=True, unique=True)
    type = WeakForeignKey('IdentifierType', verbose_name=_('type'))
    date_add = DateTimeField(_('date added'), auto_now_add=True)
    date_first = DateTimeField(_('date of first attribution'))
    date_last = DateTimeField(_('date of last attribution'))
    date_modified = DateTimeField(_('date modified'), auto_now=True)
    notes = TextField(_('notes'))

    class Meta(MetaCore):
        abstract = True
        ordering = ['-date_last']

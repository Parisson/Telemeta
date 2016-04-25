# -*- coding: utf-8 -*-
# Copyright (C) 2007-2010 Samalyse SARL
# Copyright (C) 2010-2011 Parisson SARL

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
from django.utils.translation import ugettext_lazy as _


class Instrument(ModelCore):
    "Instrument used in the item"
    name = CharField(_('name'), required=True)
    notes = TextField(_('notes'))

    class Meta(MetaCore):
        db_table = 'instruments'
        ordering = ['name']

    def __unicode__(self):
        return self.name

class InstrumentAlias(ModelCore):
    "Instrument other name"
    name = CharField(_('name'), required=True)
    notes = TextField(_('notes'))

    class Meta(MetaCore):
        db_table = 'instrument_aliases'
        verbose_name_plural = _('instrument aliases')
        ordering = ['name']

    def __unicode__(self):
        return self.name

class InstrumentRelation(ModelCore):
    "Instrument family"
    instrument = ForeignKey('Instrument', related_name="parent_relation",
                                   verbose_name=_('instrument'))
    parent_instrument = ForeignKey('Instrument', related_name="child_relation",
                                   verbose_name=_('parent instrument'))

    class Meta(MetaCore):
        db_table = 'instrument_relations'
        unique_together = (('instrument', 'parent_instrument'),)

    def __unicode__(self):
        sep = ' > '
        return self.parent_instrument.name + sep + self.instrument.name

class InstrumentAliasRelation(ModelCore):
    "Instrument family other name"
    alias = ForeignKey('InstrumentAlias', related_name="other_name",
                            verbose_name=_('alias'))
    instrument = ForeignKey('Instrument', related_name="relation",
                            verbose_name=_('instrument'))

    def __unicode__(self):
        sep = ' : '
        return self.alias.name + sep + self.instrument.name

    class Meta(MetaCore):
        db_table = 'instrument_alias_relations'
        unique_together = (('alias', 'instrument'),)


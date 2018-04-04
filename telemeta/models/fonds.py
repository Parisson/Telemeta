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

from __future__ import division
from django.utils.translation import ugettext_lazy as _
from telemeta.models.core import *
from telemeta.models.resource import *
from telemeta.models.corpus import *


class MediaFonds(MediaBaseResource):
    "Describe fonds"

    element_type = 'fonds'
    children_type = 'corpus'

    children = models.ManyToManyField(MediaCorpus, related_name="fonds",
                                      verbose_name=_('corpus'), blank=True, null=True)

    objects = MediaFondsManager()

    @property
    def public_id(self):
        return self.code

    @property
    def has_mediafile(self):
        for child in self.children.all():
            if child.has_mediafile:
                return True
        return False

    def computed_duration(self):
        duration = Duration()
        for child in self.children.all():
            duration += child.computed_duration()
        return duration
    computed_duration.verbose_name = _('total available duration')

    class Meta(MetaCore):
        db_table = 'media_fonds'
        verbose_name = _('fonds')
        verbose_name_plural = _('fonds')
        ordering = ['code']


class MediaFondsRelated(MediaRelated):
    "Fonds related media"

    resource = ForeignKey(MediaFonds, related_name="related", verbose_name=_('fonds'))

    class Meta(MetaCore):
        db_table = 'media_fonds_related'
        verbose_name = _('fonds related media')
        verbose_name_plural = _('fonds related media')



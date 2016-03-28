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
from telemeta.models.collection import *


class MediaCorpus(MediaBaseResource):
    "Describe a corpus"

    element_type = 'corpus'
    children_type = 'collections'

    children = models.ManyToManyField(MediaCollection, related_name="corpus",
                                      verbose_name=_('collections'),  blank=True, null=True)
    recorded_from_year    = IntegerField(_('recording year (from)'), help_text=_('YYYY'))
    recorded_to_year      = IntegerField(_('recording year (until)'), help_text=_('YYYY'))

    objects = MediaCorpusManager()

    permissions = (("can_download_corpus_epub", "Can download corpus EPUB"),)

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
        db_table = 'media_corpus'
        verbose_name = _('corpus')
        verbose_name_plural = _('corpus')
        ordering = ['code']


class MediaCorpusRelated(MediaRelated):
    "Corpus related media"

    resource = ForeignKey(MediaCorpus, related_name="related", verbose_name=_('corpus'))

    class Meta(MetaCore):
        db_table = 'media_corpus_related'
        verbose_name = _('corpus related media')
        verbose_name_plural = _('corpus related media')



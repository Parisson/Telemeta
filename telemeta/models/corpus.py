# -*- coding: utf-8 -*-
# Copyright (C) 2010 Samalyse SARL
# Copyright (C) 2010-2014 Parisson SARL

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


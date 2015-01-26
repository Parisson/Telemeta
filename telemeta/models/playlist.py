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


class Playlist(ModelCore):
    "Item, collection or marker playlist"
    element_type = 'playlist'
    public_id      = CharField(_('public_id'), required=True)
    author         = ForeignKey(User, related_name="playlists", db_column="author")
    title          = CharField(_('title'), required=True)
    description    = TextField(_('description'))

    class Meta(MetaCore):
        db_table = 'playlists'

    def __unicode__(self):
        return self.title


class PlaylistResource(ModelCore):
    "Playlist components"
    RESOURCE_TYPE_CHOICES = (('item', 'item'), ('collection', 'collection'),
                             ('marker', 'marker'), ('fonds', 'fonds'), ('corpus', 'corpus'))
    element_type       = 'playlist_resource'
    public_id          = CharField(_('public_id'), required=True)
    playlist           = ForeignKey('Playlist', related_name="resources", verbose_name=_('playlist'))
    resource_type      = CharField(_('resource_type'), choices=RESOURCE_TYPE_CHOICES, required=True)
    resource_id        = CharField(_('resource_id'), required=True)

    class Meta(MetaCore):
        db_table = 'playlist_resources'



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



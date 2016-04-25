# -*- coding: utf-8 -*-
# Copyright (C) 2010-2012 Parisson SARL

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

# Authors: Guillaume Pellerin <yomguy@parisson.com>


from telemeta.views.core import *


class MarkerView(object):
    """Provide Collections web UI methods"""

    @jsonrpc_method('telemeta.add_marker')
    def add_marker(request, marker):
        # marker must be a dict
        if isinstance(marker, dict):
            item_id = marker['item_id']
            item = MediaItem.objects.get(id=item_id)
            m = MediaItemMarker(item=item)
            m.public_id = marker['public_id']
            m.time = float(marker['time'])
            m.title = marker['title']
            m.description = marker['description']
            m.author = User.objects.get(username=marker['author'])
            m.save()
            m.set_revision(request.user)
        else:
            raise 'Error : Bad marker dictionnary'

    @jsonrpc_method('telemeta.del_marker')
    def del_marker(request, public_id):
        m = MediaItemMarker.objects.get(public_id=public_id)
        m.delete()

    @jsonrpc_method('telemeta.get_markers')
    def get_markers(request, item_id):
        item = MediaItem.objects.get(id=item_id)
        markers = MediaItemMarker.objects.filter(item=item)
        list = []
        for marker in markers:
            dict = {}
            dict['public_id'] = marker.public_id
            dict['time'] = str(marker.time)
            dict['title'] = marker.title
            dict['description'] = marker.description
            dict['author'] = marker.author.username
            list.append(dict)
        return list

    @jsonrpc_method('telemeta.update_marker')
    def update_marker(request, marker):
        if isinstance(marker, dict):
            m = MediaItemMarker.objects.get(public_id=marker['public_id'])
            m.time = float(marker['time'])
            m.title = marker['title']
            m.description = marker['description']
            m.save()
            m.set_revision(request.user)
        else:
            raise 'Error : Bad marker dictionnary'

    @jsonrpc_method('telemeta.get_marker_id')
    def get_marker_id(request, public_id):
        marker = MediaItemMarker.objects.get(public_id=public_id)
        return marker.id



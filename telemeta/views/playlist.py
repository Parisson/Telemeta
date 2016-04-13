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
import json
from django.http import HttpResponse


class PlaylistView(object):
    """Provide Playlist web UI methods"""

    @jsonrpc_method('telemeta.add_playlist')
    def add_playlist(request, playlist):
        # playlist must be a dict
        if isinstance(playlist, dict):
            m = Playlist()
            m.public_id = playlist['public_id']
            m.title = playlist['title']
            m.description = playlist['description']
            m.author = request.user
            m.save()
        else:
            raise 'Error : Bad playlist dictionnary'

    @jsonrpc_method('telemeta.del_playlist')
    def del_playlist(request, public_id):
        m = Playlist.objects.get(public_id=public_id)
        m.delete()

    @jsonrpc_method('telemeta.update_playlist')
    def update_playlist(request, playlist):
        if isinstance(playlist, dict):
            m = Playlist.objects.get(public_id=playlist['public_id'])
            m.title = playlist['title']
            m.description = playlist['description']
            m.save()
        else:
            raise 'Error : Bad playlist dictionnary'

    @jsonrpc_method('telemeta.add_playlist_resource')
    def add_playlist_resource(request, playlist_id, playlist_resource):
        # playlist_resource must be a dict
        if isinstance(playlist_resource, dict):
            m = PlaylistResource()
            m.public_id = playlist_resource['public_id']
            m.playlist = Playlist.objects.get(public_id=playlist_id, author=request.user)
            m.resource_type = playlist_resource['resource_type']
            m.resource_id = playlist_resource['resource_id']
            m.save()
        else:
            raise 'Error : Bad playlist_resource dictionnary'

    @jsonrpc_method('telemeta.del_playlist_resource')
    def del_playlist_resource(request, public_id, playlist_range):
        m = PlaylistResource.objects.get(public_id=public_id)
        m.delete()
        return playlist_range

    def get_elements(self, playlist, resource_type):
        resources = PlaylistResource.objects.filter(playlist=playlist)
        elements = []
        for resource in resources:
            if resource_type == 'items':
                if resource.resource_type == 'collection':
                    collections = MediaCollection.objects.filter(id=resource.resource_id)
                    if collections:
                        collection = collections[0]
                        collection_items = MediaItem.objects.filter(collection=collection)
                        for item in collection_items:
                            elements.append(item)
                elif resource.resource_type == 'item':
                    items = MediaItem.objects.filter(id=resource.resource_id)
                    if items:
                        item = items[0]
                        elements.append(item)
            elif resource_type == 'collections':
                if resource.resource_type == 'collection':
                    collection = MediaCollection.objects.get(id=resource.resource_id)
                    elements.append(collection)
        return elements

    def playlist_csv_export(self, request, public_id, resource_type):
        playlist = Playlist.objects.get(public_id=public_id)
        elements = self.get_elements(playlist, resource_type)
        pseudo_buffer = Echo()
        writer = UnicodeCSVWriter(pseudo_buffer, elements)
        response = StreamingHttpResponse(writer.output(), content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename='+playlist.title+'_'+resource_type+'.csv'
        return response

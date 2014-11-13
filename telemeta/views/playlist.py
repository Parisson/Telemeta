# -*- coding: utf-8 -*-
# Copyright (C) 2010-2012 Parisson SARL

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

# Authors: Guillaume Pellerin <yomguy@parisson.com>


from telemeta.views.core import *


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
    def del_playlist_resource(request, public_id):
        m = PlaylistResource.objects.get(public_id=public_id)
        m.delete()


    def playlist_csv_export(self, request, public_id, resource_type):
        playlist = Playlist.objects.get(public_id=public_id, author=request.user)
        resources = PlaylistResource.objects.filter(playlist=playlist)
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename='+playlist.title+'_'+resource_type+'.csv'
        writer = UnicodeWriter(response)

        elements = []
        for resource in resources:
            if resource_type == 'items':
                if resource.resource_type == 'collection':
                    collection = MediaCollection.objects.get(id=resource.resource_id)
                    collection_items = MediaItem.objects.filter(collection=collection)
                    for item in collection_items:
                        elements.append(item)
                elif resource.resource_type == 'item':
                    item = MediaItem.objects.get(id=resource.resource_id)
                    elements.append(item)

            elif resource_type == 'collections':
                if resource.resource_type == 'collection':
                    collection = MediaCollection.objects.get(id=resource.resource_id)
                    elements.append(collection)

        if elements:
            element = elements[0].to_dict()
            tags = element.keys()
            # code and title on the two first column
            tags.remove('code')
            tags.remove('title')
            tags.sort()
            tags.insert(0, 'title')
            tags.insert(0, 'code')
            writer.writerow(tags)

            for element in elements:
                data = []
                element = element.to_dict()
                for tag in tags:
                    data.append(element[tag])
                writer.writerow(data)

        return response


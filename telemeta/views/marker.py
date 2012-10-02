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

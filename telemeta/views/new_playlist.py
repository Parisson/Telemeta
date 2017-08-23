# -*- coding: utf-8 -*-
from telemeta.views.core import *
from telemeta.models import *
import uuid

class NewPlaylistView(object):

    def display(self, request, type="item"):

        self.type=type

        template_name = loader.get_template('telemeta/search/addplaylist.html')

        idlist = request.POST.getlist('selected_items_list')
        itemlist = []
        if self.type =="item":
            for itemid in idlist:
                itemlist.append(MediaItem.objects.all().get(id=itemid))

        if self.type =="collection":
            for itemid in idlist:
                itemlist.append(MediaCollection.objects.all().get(id=itemid))

        context = RequestContext(request, {
                'selected_items_list': itemlist,
                'existing_playlists': Playlist.objects.all().filter(author=request.user),
                'type':self.type,
                'lastquerypath':request.POST.get('lastquerypath')})
        return HttpResponse(template_name.render(context))

    def addToPlaylist(self, request, type=None):
        self.type=type

        template_name = loader.get_template('telemeta/search/confirmation_add_playslist.html')

        idlist = request.POST.getlist('item_id')
        selected_playlist_id = request.POST.get('playlist_id')
        selected_playlist = Playlist.objects.all().get(id=selected_playlist_id)

        itemlist = []
        if self.type == "item":
            for itemid in idlist:
                itemlist.append(MediaItem.objects.all().get(id=itemid))

            for item in itemlist:
                new_id = uuid.uuid4()
                PlaylistResource.objects.get_or_create(resource_type='item',resource_id=item.id,playlist=selected_playlist,defaults={'public_id':new_id})
        else:
            for itemid in idlist:
                itemlist.append(MediaCollection.objects.all().get(id=itemid))

            for item in itemlist:
                new_id = uuid.uuid4()
                PlaylistResource.objects.get_or_create(resource_type='collection',resource_id=item.id,playlist=selected_playlist,defaults={'public_id':new_id})

        context = RequestContext(request, {
                'selected_items_list': itemlist,
                'type':self.type,
                'lastquerypath': request.POST.get('lastquerypath')})
        return HttpResponse(template_name.render(context))

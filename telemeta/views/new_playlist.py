# -*- coding: utf-8 -*-
from telemeta.views.core import *
from telemeta.models import *

class NewPlaylistView(object):

    def display(self, request):

        template_name = loader.get_template('search/addplaylist.html')

        idlist = request.POST.getlist('selected_items_list')
        itemlist = []
        for itemid in idlist:
            itemlist.append(MediaItem.objects.all().get(id=itemid))
        context = RequestContext(request, {
                'selected_items_list': itemlist,
                'existing_playlists': Playlist.objects.all().filter(author=request.user),
                'lastquerypath':request.POST.get('lastquerypath')})
        return HttpResponse(template_name.render(context))

    def addToPlaylist(self, request):
        template_name = loader.get_template('search/confirmation_add_playslist.html')

        idlist = request.POST.getlist('item_id')
        selected_playlist_id = request.POST.get('playlist_id')
        selected_playlist = Playlist.objects.all().get(id=selected_playlist_id)

        itemlist = []
        for itemid in idlist:
            itemlist.append(MediaItem.objects.all().get(id=itemid))

        for item in itemlist:
            resource = PlaylistResource.objects.get_or_create(resource_type='item',public_id='4567891542',resource_id=item.id,playlist=selected_playlist)

        context = RequestContext(request, {
                'selected_items_list': itemlist,
                'lastquerypath': request.POST.get('lastquerypath')})
        return HttpResponse(template_name.render(context))



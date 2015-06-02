# -*- coding: utf-8 -*-
from telemeta.views.core import *
from telemeta.models import *

class NewPlaylistView(TemplateView):
    template_name = 'search/addplaylist.html'
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(NewPlaylistView, self).get_context_data(**kwargs)
        # Add in the publisher
        idlist = self.request.GET.getlist('selected_items_list')
        itemlist = []
        for itemid in idlist:
            itemlist.append(MediaItem.objects.all().get(id=itemid))
        context['selected_items_list'] = itemlist
        return context
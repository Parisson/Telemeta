from django.conf.urls.defaults import *
from telemeta.models import MediaItem

list_dict = {
    'queryset': MediaItem.objects.all(),
}

urlpatterns = patterns('',
    (r'^$', 'telemeta.views.web.index'),
    (r'^media_item/$', 'django.views.generic.list_detail.object_list', 
        dict(list_dict, paginate_by=10, template_name="mediaitem_list.html")),
    (r'^media_item/(?P<media_item_id>[0-9]+)/$', 'telemeta.views.web.media_item_edit'),
    (r'^media_item/(?P<media_item_id>[0-9]+)/update/$', 'telemeta.views.web.media_item_update'),

    # CSS (FIXME: for developement only)
    (r'^css/(?P<path>.*)$', 'django.views.static.serve', {'document_root': './telemeta/css'}),
)



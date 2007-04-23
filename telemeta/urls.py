from django.conf.urls.defaults import *
from telemeta.models import MediaItem, MediaCollection

all_items = {
    'queryset': MediaItem.objects.all(),
}

all_collections = {
    'queryset': MediaCollection.objects.all(),
}

urlpatterns = patterns('',
    (r'^$', 'telemeta.views.web.index'),
    (r'^items/$', 'django.views.generic.list_detail.object_list', 
        dict(all_items, paginate_by=10, template_name="mediaitem_list.html")),
    (r'^items/(?P<item_id>[0-9]+)/$', 'telemeta.views.web.item_detail'),
    (r'^items/(?P<item_id>[0-9]+)/download/(?P<format>[0-9A-Z]+)/$', 
        'telemeta.views.web.item_export'),
    #(r'^media_item/(?P<media_item_id>[0-9]+)/$', 'telemeta.views.web.media_item_edit'),
    (r'^media_item/(?P<media_item_id>[0-9]+)/update/$', 'telemeta.views.web.media_item_update'),

    (r'^collections/$', 'django.views.generic.list_detail.object_list',
        dict(all_collections, paginate_by=10, template_name="collection_list.html")),
    (r'^collections/(?P<object_id>[0-9]+)/$', 
        'django.views.generic.list_detail.object_detail',
        dict(all_collections, template_name="collection_detail.html")),

    (r'^search/$', 
        'telemeta.views.web.quick_search'),


    # CSS (FIXME: for developement only)
    (r'^css/(?P<path>.*)$', 'django.views.static.serve', {'document_root': './telemeta/css'}),
)



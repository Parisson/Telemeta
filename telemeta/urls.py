# Copyright (C) 2007 Samalyse SARL
# All rights reserved.
#
# This software is licensed as described in the file COPYING, which
# you should have received as part of this distribution. The terms
# are also available at http://svn.parisson.org/telemeta/TelemetaLicense.
#
# Author: Olivier Guilyardi <olivier@samalyse.com>

from django.conf.urls.defaults import *
from telemeta.models import MediaItem, MediaCollection
from telemeta.core import ComponentManager
from telemeta.web import WebView
import os.path

# initialization
comp_mgr = ComponentManager()
web_view = WebView(comp_mgr)

# query sets for Django generic views
all_items = { 'queryset': MediaItem.objects.all(), }
all_collections = { 'queryset': MediaCollection.objects.all(), }

# ID's regular expressions
i_ex = MediaItem.id_regex
c_ex = MediaCollection.id_regex
export_extensions = "|".join(web_view.list_export_extensions())

htdocs = os.path.dirname(__file__) + '/htdocs'

urlpatterns = patterns('',
    url(r'^$', web_view.index, name="telemeta-home"),

    # items
    url(r'^items/$', 'django.views.generic.list_detail.object_list', 
        dict(all_items, paginate_by=20, template_name="mediaitem_list.html"),
        name="telemeta-items"),
    url(r'^items/(?P<item_id>' + i_ex + ')/$', web_view.item_detail, 
        name="telemeta-item-detail"),
    url(r'^items/(?P<item_id>' + i_ex + ')/dc/$', web_view.item_detail, 
        {'template': 'mediaitem_detail_dc.html'},
        name="telemeta-item-dublincore"),
    url(r'^items/(?P<item_id>' + i_ex + ')/dc/xml/$', web_view.item_detail, 
        {'format': 'dublin_core_xml'},
        name="telemeta-item-dublincore-xml"),
    url(r'^items/download/(?P<item_id>' + i_ex + ').(?P<extension>' 
            + export_extensions + ')$', 
        web_view.item_export,
        name="telemeta-item-export"),
    url(r'^items/(?P<item_id>' + i_ex + ')/visualize/(?P<visualizer_id>[0-9a-z_]+)/$', 
        web_view.item_visualize,
        name="telemeta-item-visualize"),
    url(r'^items/(?P<item_id>' + i_ex + ')/item_xspf.xml$', 
        web_view.item_playlist, 
        dict(template="mediaitem_xspf.xml", mimetype="application/xspf+xml"),
        name="telemeta-item-xspf"),

    # collections
    url(r'^collections/$', 'django.views.generic.list_detail.object_list',
        dict(all_collections, paginate_by=20, 
            template_name="collection_list.html"),
        name="telemeta-collections"),
    url(r'^collections/?page=(?P<page>[0-9]+)$', 
        'django.views.generic.list_detail.object_list',
        dict(all_collections, paginate_by=20)),
    url(r'^collections/(?P<object_id>' + c_ex + ')/$', 
        'django.views.generic.list_detail.object_detail',
        dict(all_collections, template_name="collection_detail.html"),
        name="telemeta-collection-detail"),
    url(r'^collections/(?P<object_id>' + c_ex + ')/dc/$', 
        'django.views.generic.list_detail.object_detail',
        dict(all_collections, template_name="collection_detail_dc.html"),
        name="telemeta-collection-dublincore"),
    url(r'^collections/(?P<collection_id>' + c_ex + ')/collection_xspf.xml$', 
        web_view.collection_playlist, 
        dict(template="collection_xspf.xml", mimetype="application/xspf+xml"),
        name="telemeta-collection-xspf"),
    url(r'^collections/(?P<collection_id>' + c_ex + ')/collection.m3u$',
        web_view.collection_playlist, 
        dict(template="collection.m3u", mimetype="audio/mpegurl"),
        name="telemeta-collection-m3u"),

    # search
    url(r'^search/$', web_view.search, name="telemeta-search"),
    url(r'^search/criteria/$', web_view.edit_search, name="telemeta-search-criteria"),

    # administration        
    url(r'^admin/$', web_view.admin_index, name="telemeta-admin"),        

    # enumerations administration
    url(r'^admin/enumerations/(?P<enumeration_id>[0-9a-z]+)/$', 
        web_view.edit_enumeration ,
        name="telemeta-enumeration-edit"),        
    url(r'^admin/enumerations/(?P<enumeration_id>[0-9a-z]+)/add/$', 
        web_view.add_to_enumeration,
        name="telemeta-enumeration-add"),        
    url(r'^admin/enumerations/(?P<enumeration_id>[0-9a-z]+)/update/$', 
        web_view.update_enumeration,
        name="telemeta-enumeration-update"),        
    url(r'^admin/enumerations/(?P<enumeration_id>[0-9a-z]+)/'
        + r'(?P<value_id>[0-9]+)/$',
        web_view.edit_enumeration_value,
        name="telemeta-enumeration-record-edit"),   
    url(r'^admin/enumerations/(?P<enumeration_id>[0-9a-z]+)/'
        + r'(?P<value_id>[0-9]+)/update/$',
        web_view.update_enumeration_value, 
        name="telemeta-enumeration-record-update"),   

    # Geographic browsing
    url(r'geo/$', web_view.list_continents, name="telemeta-geo-continents"),
    url(r'geo/(?P<continent>[A-Za-z]+)/$', web_view.list_countries, 
        name="telemeta-geo-countries"),
    url('geo/(?P<continent>[A-Za-z]+)/(?P<country>[-A-Za-z0-9%;.,"& \']+)/$', 
        web_view.list_country_collections, 
        name="telemeta-geo-country-collections"),
    url(r'dynjs/continents.js$', web_view.get_continents_js, name="telemeta-continents-js"),

    # CSS+Images (FIXME: for developement only)
    url(r'css/(?P<path>.*)$', 'django.views.static.serve', 
        {'document_root': htdocs+'/css'},
        name="telemeta-css"),
    url(r'images/(?P<path>.*)$', 'django.views.static.serve', 
        {'document_root': htdocs+'/images'},
        name="telemeta-images"),
    url(r'js/(?P<path>.*)$', 'django.views.static.serve', 
        {'document_root': htdocs+'/js'},
        name="telemeta-js"),
    url(r'swf/(?P<path>.*)$', 'django.views.static.serve', 
        {'document_root': htdocs+'/swf'},
        name="telemeta-swf"),
)

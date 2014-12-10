# -*- coding: utf-8 -*-
# Copyright (C) 2007 Samalyse SARL
# Copyright (c) 2007-2011 Parisson SARL

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
#
# Authors: Olivier Guilyardi <olivier@samalyse.com>
#          Guillaume Pellerin <yomguy@parisson.com>

from django.conf.urls import patterns, url, include
from django.conf import settings
from django.views.generic import RedirectView
from django.views.generic.list import ListView
from telemeta.models import MediaItem, MediaCollection, MediaItemMarker, MediaCorpus, MediaFonds
from telemeta.views import *
#from telemeta.views import HomeView, AdminView, CollectionView, ItemView, \
#                            InstrumentView, InstrumentAliasView, PlaylistView, ProfileView, GeoView, \
#                            LastestRevisionsFeed, ResourceView, UserRevisionsFeed, CollectionPackageView
from jsonrpc import jsonrpc_site
import os.path
import telemeta.config

telemeta.config.check()

# initialization
home_view = HomeView()
admin_view = AdminView()
collection_view = CollectionView()
item_view = ItemView()
instrument_view = InstrumentView()
instrument_alias_view = InstrumentAliasView()
playlist_view = PlaylistView()
profile_view = ProfileView()
geo_view = GeoView()
resource_view = ResourceView()

# ID's regular expressions
export_extensions = "|".join(item_view.list_export_extensions())


urlpatterns = patterns('',
    url(r'^$', home_view.home, name="telemeta-home"),

    # items
    url(r'^archives/items/$', ItemListView.as_view(), name="telemeta-items"),
    url(r'^archives/items_sound/$', ItemSoundListView.as_view(), name="telemeta-items-sound"),
    url(r'^archives/items_unpublished/$', ItemUnpublishedListView.as_view(), name="telemeta-items-unpublished"),
    url(r'^archives/items_published/$', ItemPublishedListView.as_view(), name="telemeta-items-published"),

    url(r'^archives/items/(?P<public_id>[A-Za-z0-9._-]+)/$', ItemDetailView.as_view(), name="telemeta-item-detail"),
    url(r'^archives/items/(?P<public_id>[A-Za-z0-9._-]+)/dc/$', item_view.item_detail, {'template': 'telemeta/mediaitem_detail_dc.html'}, name="telemeta-item-dublincore"),
    url(r'^archives/items/(?P<public_id>[A-Za-z0-9._-]+)/dc/xml/$', item_view.item_detail, {'format': 'dublin_core_xml'}, name="telemeta-item-dublincore-xml"),
    url(r'^archives/items/download/(?P<public_id>[A-Za-z0-9._-]+)\.(?P<extension>' + export_extensions + ')$', item_view.item_export, name="telemeta-item-export"),
    url(r'^archives/items/(?P<public_id>[A-Za-z0-9._-]+)/visualize/(?P<grapher_id>[0-9a-z_]+)/(?P<width>[0-9A-Z]+)x(?P<height>[0-9A-Z]+)/$', item_view.item_visualize, name="telemeta-item-visualize"),
    url(r'^archives/items/(?P<public_id>[A-Za-z0-9._-]+)/analyze/xml/$', item_view.item_analyze_xml, name="telemeta-item-analyze-xml"),
    url(r'^archives/items/(?P<public_id>[A-Za-z0-9._-]+)/item_xspf.xml$', item_view.item_playlist, dict(template="telemeta/mediaitem_xspf.xml", mimetype="application/xspf+xml"), name="telemeta-item-xspf"),
    url(r'^archives/items/(?P<public_id>[A-Za-z0-9._-]+)/edit/$', ItemEditView.as_view(), name="telemeta-item-edit"),
    url(r'^archives/items/(?P<public_id>[A-Za-z0-9._-]+)/copy/$', ItemCopyView.as_view(), name="telemeta-item-copy"),
    url(r'^archives/items_add/$', ItemAddView.as_view(), name="telemeta-item-add"),
    url(r'^archives/items/(?P<public_id>[A-Za-z0-9._-]+)/player/(?P<width>[0-9]+)x(?P<height>[0-9]+)/$', item_view.item_detail, dict(template='telemeta/mediaitem_player.html'), name="telemeta-item-player"),
    url(r'^archives/items/(?P<public_id>[A-Za-z0-9._-]+)/player/(?P<width>[0-9]+)x(?P<height>[0-9]+)/simple/$', item_view.item_detail, dict(template='telemeta/mediaitem_player_simple.html'), name="telemeta-item-player-simple"),
    url(r'^archives/items/(?P<public_id>[A-Za-z0-9._-]+)/player/(?P<width>[0-9]+)x(?P<height>[0-9]+)/countour/$', item_view.item_detail, dict(template='telemeta/mediaitem_player_contour.html'), name="telemeta-item-player-contour"),
    url(r'^archives/items/(?P<public_id>[A-Za-z0-9._-]+)/delete/$', item_view.item_delete, name="telemeta-item-delete"),
    url(r'^archives/items/(?P<item_public_id>[A-Za-z0-9._-]+)/related/(?P<media_id>[A-Za-z0-9._-]+)/view/$', item_view.related_media_item_stream, name="telemeta-item-related"),
    url(r'^archives/items/(?P<item_public_id>[A-Za-z0-9._-]+)/related/(?P<media_id>[A-Za-z0-9._-]+)/download/$', item_view.related_media_item_download, name="telemeta-item-related-download"),

    # Markers
    url(r'^archives/markers/(?P<marker_id>[A-Za-z0-9]+)/$', item_view.item_detail, name="telemeta-item-detail-marker"),

    # FIXME: need all paths
    url(r'^items/(?P<path>[A-Za-z0-9._-s/]+)/$', RedirectView.as_view(), {'url': '/archives/items/%(path)s/', 'permanent': False}, name="telemeta-item-redir"),

    # collections
    url(r'^archives/collections/$', CollectionListView.as_view(), name="telemeta-collections"),
    url(r'^archives/collections_unpublished/$', CollectionUnpublishedListView.as_view(), name="telemeta-collections-unpublished"),
    url(r'^archives/collections_published/$', CollectionPublishedListView.as_view(), name="telemeta-collections-published"),
    url(r'^archives/collections_sound/$', CollectionSoundListView.as_view(), name="telemeta-collections-sound"),
    url(r'^archives/collections/(?P<public_id>[A-Za-z0-9._-]+)/$', CollectionDetailView.as_view(), name="telemeta-collection-detail"),
    url(r'^archives/collections/(?P<public_id>[A-Za-z0-9._-]+)/dc/$', CollectionDetailViewDC.as_view(), name="telemeta-collection-dublincore"),
    # url(r'^archives/collections/(?P<public_id>[A-Za-z0-9._-]+)/collection_xspf.xml$', collection_view.collection_playlist, dict(template="telemeta/collection_xspf.xml", mimetype="application/xspf+xml"), name="telemeta-collection-xspf"),
    # url(r'^archives/collections/(?P<public_id>[A-Za-z0-9._-]+)/collection.m3u$', collection_view.collection_playlist, dict(template="telemeta/collection.m3u", mimetype="audio/mpegurl"), name="telemeta-collection-m3u"),
    url(r'^archives/collections/(?P<public_id>[A-Za-z0-9._-]+)/edit/$', CollectionEditView.as_view(), name="telemeta-collection-edit"),
    url(r'^archives/collections/(?P<public_id>[A-Za-z0-9._-]+)/copy/$', CollectionCopyView.as_view(), name="telemeta-collection-copy"),
    url(r'^archives/collections_add/$', CollectionAddView.as_view(), name="telemeta-collection-add"),
    url(r'^archives/collections/(?P<public_id>[A-Za-z0-9._-]+)/add_item/$', ItemAddView.as_view(), name="telemeta-collection-additem"),
    url(r'^archives/collections/(?P<public_id>[A-Za-z0-9._-]+)/delete/$', collection_view.collection_delete, name="telemeta-collection-delete"),
    url(r'^archives/collections/(?P<collection_public_id>[A-Za-z0-9._-]+)/related/(?P<media_id>[A-Za-z0-9._-]+)/view/$', collection_view.related_media_collection_stream, name="telemeta-collection-related"),
    url(r'^archives/collections/(?P<collection_public_id>[A-Za-z0-9._-]+)/related/(?P<media_id>[A-Za-z0-9._-]+)/download/$', collection_view.related_media_collection_download, name="telemeta-collection-related-download"),

    # FIXME: need all paths
    url(r'^collections/(?P<path>[A-Za-z0-9._-s/]+)/$', RedirectView.as_view(), {'url': '/archives/collections/%(path)s/', 'permanent': False}, name="telemeta-collection-redir"),
    url(r'^archives/collections/(?P<public_id>[A-Za-z0-9._-]+)/package/$', CollectionPackageView.as_view(),
        name="telemeta-collection-package"),

    # Generic resources
    url(r'^archives/(?P<type>[A-Za-z0-9._-]+)/$', ResourceListView.as_view(), name="telemeta-resource-list"),
    url(r'^archives/(?P<type>[A-Za-z0-9._-]+)/(?P<public_id>[A-Za-z0-9._-]+)/$', ResourceDetailView.as_view(), name="telemeta-resource-detail"),
    url(r'^archives/(?P<type>[A-Za-z0-9._-]+)/(?P<public_id>[A-Za-z0-9._-]+)/edit/$', ResourceEditView.as_view(), name="telemeta-resource-edit"),
    url(r'^archives/(?P<type>[A-Za-z0-9._-]+)/(?P<public_id>[A-Za-z0-9._-]+)/dc/$', ResourceDetailDCView.as_view(), name="telemeta-resource-dublincore"),
    url(r'^archives/(?P<type>[A-Za-z0-9._-]+)/(?P<public_id>[A-Za-z0-9._-]+)/copy/$', ResourceCopyView.as_view(), name="telemeta-resource-copy"),
    url(r'^archives/(?P<type>[A-Za-z0-9._-]+)_add$', ResourceAddView.as_view(), name="telemeta-resource-add"),
    url(r'^archives/(?P<type>[A-Za-z0-9._-]+)/(?P<public_id>[A-Za-z0-9._-]+)/delete/$', ResourceDeleteView.as_view(), name="telemeta-resource-delete"),
    url(r'^archives/(?P<type>[A-Za-z0-9._-]+)/(?P<public_id>[A-Za-z0-9._-]+)/related/(?P<media_id>[A-Za-z0-9._-]+)/view/$', resource_view.related_stream, name="telemeta-resource-related"),
    url(r'^archives/(?P<type>[A-Za-z0-9._-]+)/(?P<public_id>[A-Za-z0-9._-]+)/related/(?P<media_id>[A-Za-z0-9._-]+)/download/$', resource_view.related_download, name="telemeta-resource-related-download"),

    # search
    # url(r'^archives/$', home_view.search, name="telemeta-archives"),
    url(r'^search/$', SearchView.as_view(), name="telemeta-search"),
    url(r'^search/(?P<type>[A-Za-z0-9._-]+)/$', SearchView.as_view(), name="telemeta-search-type"),
    url(r'^search_criteria/$', home_view.edit_search, name="telemeta-search-criteria"),
    url(r'^complete_location/$', home_view.complete_location, name="telemeta-complete-location"),

    # administration
    url(r'^admin/$', admin_view.admin_index, name="telemeta-admin"),
    url(r'^admin/general/$', admin_view.admin_general, name="telemeta-admin-general"),
    url(r'^admin/enumerations/$', admin_view.admin_enumerations, name="telemeta-admin-enumerations"),
    url(r'^admin/users/$', admin_view.admin_users, name="telemeta-admin-users"),

    # instruments administration
    url(r'^admin/instruments/$', instrument_view.edit_instrument , name="telemeta-instrument-edit"),
    url(r'^admin/instruments/add/$', instrument_view.add_to_instrument, name="telemeta-instrument-add"),
    url(r'^admin/instruments/update/$', instrument_view.update_instrument, name="telemeta-instrument-update"),
    url(r'^admin/instruments/' + r'(?P<value_id>[0-9]+)/$', instrument_view.edit_instrument_value, name="telemeta-instrument-record-edit"),
    url(r'^admin/instruments/' + r'(?P<value_id>[0-9]+)/update/$', instrument_view.update_instrument_value, name="telemeta-instrument-record-update"),
    url(r'^admin/instruments/' + r'(?P<value_id>[0-9]+)/replace/$', instrument_view.replace_instrument_value, name="telemeta-instrument-record-replace"),

    # instruments aliases administration
    url(r'^admin/instrument_aliases/$', instrument_alias_view.edit_instrument, name="telemeta-instrument-alias-edit"),
    url(r'^admin/instrument_aliases/add/$', instrument_alias_view.add_to_instrument, name="telemeta-instrument-alias-add"),
    url(r'^admin/instrument_aliases/update/$', instrument_alias_view.update_instrument, name="telemeta-instrument-alias-update"),
    url(r'^admin/instrument_aliases/' + r'(?P<value_id>[0-9]+)/$', instrument_alias_view.edit_instrument_value, name="telemeta-instrument-alias-record-edit"),
    url(r'^admin/instrument_aliases/' + r'(?P<value_id>[0-9]+)/update/$', instrument_alias_view.update_instrument_value, name="telemeta-instrument-alias-record-update"),
    url(r'^admin/instrument_aliases/' + r'(?P<value_id>[0-9]+)/replace/$', instrument_alias_view.replace_instrument_value, name="telemeta-instrument-alias-record-replace"),

    # enumerations administration
    url(r'^admin/enumerations/(?P<enumeration_id>[0-9a-z]+)/$', admin_view.edit_enumeration , name="telemeta-enumeration-edit"),
    url(r'^admin/enumerations/(?P<enumeration_id>[0-9a-z]+)/add/$', admin_view.add_to_enumeration, name="telemeta-enumeration-add"),
    url(r'^admin/enumerations/(?P<enumeration_id>[0-9a-z]+)/update/$', admin_view.update_enumeration, name="telemeta-enumeration-update"),
    url(r'^admin/enumerations/(?P<enumeration_id>[0-9a-z]+)/' + r'(?P<value_id>[0-9]+)/$', admin_view.edit_enumeration_value, name="telemeta-enumeration-record-edit"),
    url(r'^admin/enumerations/(?P<enumeration_id>[0-9a-z]+)/' + r'(?P<value_id>[0-9]+)/update/$', admin_view.update_enumeration_value, name="telemeta-enumeration-record-update"),
    url(r'^admin/enumerations/(?P<enumeration_id>[0-9a-z]+)/' + r'(?P<value_id>[0-9]+)/replace/$', admin_view.replace_enumeration_value, name="telemeta-enumeration-replace"),

    # Geographic browsing
    url(r'^geo/$', geo_view.list_continents, name="telemeta-geo-continents"),
    url(r'^geo/(?P<continent>[a-z_]+)/$', geo_view.list_countries, name="telemeta-geo-countries"),
    url(r'^geo/collections/(?P<continent>[a-z_]+)/(?P<country>[a-z_]+)/$', GeoCountryCollectionView.as_view(), name="telemeta-geo-country-collections"),
    url(r'^geo/items/(?P<continent>[a-z_]+)/(?P<country>[a-z_]+)/$', GeoCountryItemView.as_view() , name="telemeta-geo-country-items"),
    url(r'^geo/country_info/(?P<id>[0-9a-z]+)/$', geo_view.country_info, name="telemeta-country-info"),

    # Flat pages
    url(r'^pages/(?P<path>.*)$', home_view.render_flatpage, name="telemeta-flatpage"),

    # OAI-PMH Data Provider
    url(r'^oai/.*$', home_view.handle_oai_request, name="telemeta-oai"),

    # Authentication
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'telemeta/login.html'}, name="telemeta-login"),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'telemeta/login.html'}, name="telemeta-login"),
    #url(r'^login/$', 'ipauth.views.login', {'template_name': 'telemeta/login.html'},
    #    name="telemeta-login"),
    url(r'^logout/$', home_view.logout, name="telemeta-logout"),

    # Users
    url(r'^accounts/$', home_view.users, name="telemeta-users"),

    # Desk
    url(r'^desk/lists/$', home_view.lists, name="telemeta-desk-lists"),
    url(r'^desk/profile/(?P<username>[A-Za-z0-9@+._-]+)/$', profile_view.profile_detail, name="telemeta-desk-profile"),
    url(r'^desk/home/$', home_view.home, name="telemeta-desk-home"),

    # Profiles
    url(r'^accounts/(?P<username>[A-Za-z0-9._-]+)/profile/$', profile_view.profile_detail, name="telemeta-profile-detail"),
    url(r'^users/(?P<username>[A-Za-z0-9._-]+)/$', profile_view.profile_detail, name="telemeta-profile-detail-2"),
    url(r'^accounts/(?P<username>[A-Za-z0-9._-]+)/profile/edit/$', profile_view.profile_edit, name="telemeta-profile-edit"),
    url(r'^accounts/(?P<username>[A-Za-z0-9._-]+)/rss/$', UserRevisionsFeed(),  name="telemeta-user-rss"),

    # Registration
    url(r'^accounts/password_change/$', 'django.contrib.auth.views.password_change', {'template_name': 'telemeta/registration/password_change_form.html'}, name="telemeta-password-change"),
    url(r'^accounts/password_change_done/$', 'django.contrib.auth.views.password_change_done', {'template_name': 'telemeta/registration/password_change_done.html'}, name="telemeta-password-change-done"),

    url(r'^accounts/password_reset/$', 'django.contrib.auth.views.password_reset', {'template_name': 'telemeta/registration/password_reset_form.html', 'email_template_name': 'telemeta/registration/password_reset_email.html'}, name="telemeta-password-reset"),
    url(r'^accounts/password_reset_done/$', 'django.contrib.auth.views.password_reset_done', {'template_name': 'telemeta/registration/password_reset_done.html'}, name="telemeta-password-reset-done"),
    url(r'^accounts/password_reset_confirm/(?P<uidb36>[A-Za-z0-9._-]+)/(?P<token>[A-Za-z0-9._-]+)/$', 'django.contrib.auth.views.password_reset_confirm', {'template_name': 'telemeta/registration/password_reset_confirm.html'}, name="telemeta-password-reset-confirm"),
    url(r'^accounts/password_reset_complete/$', 'django.contrib.auth.views.password_reset_complete', {'template_name': 'telemeta/registration/password_reset_complete.html'}, name="telemeta-password-reset-complete"),
    url(r'^accounts/password_reset_complete/$', 'django.contrib.auth.views.password_reset_complete', {'template_name': 'telemeta/registration/password_reset_complete.html'}, name="telemeta-password-reset-complete"),

    # JSON RPC
    url(r'json/$', jsonrpc_site.dispatch, name='jsonrpc_mountpoint'),

    # Playlists
    url(r'^playlists/(?P<public_id>[a-zA-Z0-9]+)/(?P<resource_type>[a-zA-Z0-9]+)/csv/$', playlist_view.playlist_csv_export, name="telemeta-playlist-csv-export"),

    # RSS feeds
    url(r'^rss/$', LastestRevisionsFeed(), name="telemeta-rss"),

    # Static media
    # FIXME:need to move export dir from the cache
    url(r'^media/cache/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.TELEMETA_CACHE_DIR,}),

    url(r'^', include('jqchat.urls')),

)

if settings.DEBUG and 'debug_toolbar' in settings.INSTALLED_APPS:
    import debug_toolbar
    urlpatterns += patterns('',
    url(r'^__debug__/', include(debug_toolbar.urls)),)
    # for the graphical browser/web console only, omissible
    url(r'json/browse/', 'jsonrpc.views.browse', name="jsonrpc_browser"),


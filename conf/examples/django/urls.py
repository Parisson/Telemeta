# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

js_info_dict = {
    'packages': ('telemeta',),
}

urlpatterns = patterns('',
    # Example:
    # (r'^sandbox/', include('sandbox.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs'
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/django/', include(admin.site.urls)),
    
    # Telemeta
    (r'^', include('telemeta.urls')),
    
    # Languages
    (r'^i18n/', include('django.conf.urls.i18n')),    
    (r'^jsi18n/$', 'django.views.i18n.javascript_catalog', js_info_dict),
)

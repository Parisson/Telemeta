# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url, include
from telemeta.views.haystack_search import *
from haystack.forms import *


urlpatterns = patterns('',
    url(r'^$', HaystackSearch(form_class=HaySearchFormItem), name='haystack_search'),
    url(r'^quick/(?P<type>[A-Za-z0-9._-]+)/$', HaystackSearch(), name='haystack_search_type'),

)

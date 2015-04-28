# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from telemeta.views.haystack_search import *
from haystack.forms import *


urlpatterns = patterns('',
    url(r'^$', HaystackSearch(), name='haystack_search'),
    url(r'^quick/(?P<type>[A-Za-z0-9._-]+)/$', HaystackSearch(), name='haystack_search_type'),
    url(r'^advance/$', HaystackAdvanceSearch(form_class=HayAdvanceForm, template='search/advanceSearch.html'), name='haystack_advance_search'),
    url(r'^advance/(?P<type>[A-Za-z0-9._-]+)/$', HaystackAdvanceSearch(form_class=HayAdvanceForm, template='search/advanceSearch.html'), name='haystack_advance_search_type'),
)

# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url, include
from telemeta.views.haystack_search import *
from haystack.query import SearchQuerySet
from haystack.views import SearchView
from haystack.forms import *
from telemeta.forms.haystack_form import HaySearchFormItem, HaySearchFormCollection, HayAdvanceSearchForm


urlpatterns = patterns('',
    url(r'^$', HaystackSearch(form_class=HaySearchFormItem), name='haystack_search'),
    url(r'^(?P<type>[A-Za-z0-9._-]+)/$', HaystackSearch(), name='haystack_search_type'),
    url(r'^advance/$', HaystackAdvanceSearch(form_class=HayAdvanceSearchForm), name='haystack_search_advance'),
)

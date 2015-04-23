# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url, include
from telemeta.views.haystack_search import *
from haystack.query import SearchQuerySet
from haystack.views import SearchView
from haystack.forms import *
from telemeta.forms.haystack_form import HaySearchFormItem, HaySearchFormCollection


urlpatterns = patterns('',
    url(r'^$', HaystackSearchItem(form_class=HaySearchFormItem), name='haystack_search_item'),
    url(r'^item/$', HaystackSearchItem(form_class=HaySearchFormItem), name='haystack_search_item'),
    url(r'^collection/$', HaystackSearchCollection(form_class=HaySearchFormCollection), name='haystack_search_collection'),
)

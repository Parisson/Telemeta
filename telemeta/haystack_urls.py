# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url, include
from telemeta.views.haystack_search import *
from haystack.query import SearchQuerySet
from haystack.views import SearchView
from telemeta.forms.haystack_form import HaySearchForm


urlpatterns = patterns('',
    url(r'^$', SearchView(form_class=HaySearchForm), name='haystack_search'),
)

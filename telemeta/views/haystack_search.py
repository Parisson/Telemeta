# -*- coding: utf-8 -*-

from haystack.views import SearchView
from haystack.query import SearchQuerySet
from telemeta.models import *
from telemeta.forms.haystack_form import HaySearchFormItem, HaySearchFormCollection

class HaystackSearchItem(SearchView):

    def get_query(self):
        return super(HaystackSearchItem, self).get_query()

    def extra_context(self):
        extra = super(HaystackSearchItem, self).extra_context()
        extra['collection_count']=SearchQuerySet().load_all().models(MediaCollection).filter(content__contains=self.get_query()).count()
        extra['item_count']=SearchQuerySet().load_all().models(MediaItem).filter(content__contains=self.get_query()).count()
        extra['type']='item'
        return extra


class HaystackSearchCollection(SearchView):

    def get_query(self):
        return super(HaystackSearchCollection, self).get_query()

    def extra_context(self):
        extra = super(HaystackSearchCollection, self).extra_context()
        extra['collection_count']=SearchQuerySet().load_all().models(MediaCollection).filter(content__contains=self.get_query()).count()
        extra['item_count']=SearchQuerySet().load_all().models(MediaItem).filter(content__contains=self.get_query()).count()
        extra['type']='collection'
        return extra

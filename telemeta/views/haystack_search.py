# -*- coding: utf-8 -*-

from haystack.views import SearchView
from haystack.query import SearchQuerySet
from telemeta.models import *
from telemeta.forms.haystack_form import HaySearchFormItem, HaySearchFormCollection

class HaystackSearch(SearchView):

    def __call__(self,request,type=None):
        self.type = type
        if(self.type=='collection'):
            self.form_class=HaySearchFormCollection
        else:
            self.form_class=HaySearchFormItem
        return super(HaystackSearch,self).__call__(request)



    def get_query(self):
        return super(HaystackSearch, self).get_query()

    def extra_context(self):
        extra = super(HaystackSearch, self).extra_context()
        extra['collection_count']=SearchQuerySet().load_all().models(MediaCollection).filter(content__contains=self.get_query()).count()
        extra['item_count']=SearchQuerySet().load_all().models(MediaItem).filter(content__contains=self.get_query()).count()
        if self.type=='collection':
            extra['type']='collection'
        else:
            extra['type']='item'
        return extra


class HaystackAdvanceSearch(SearchView):

    def get_query(self):
        return super(HaystackAdvanceSearch, self).get_query()

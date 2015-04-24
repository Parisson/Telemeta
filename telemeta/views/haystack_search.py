# -*- coding: utf-8 -*-

from haystack.views import SearchView
from haystack.query import SearchQuerySet
from telemeta.models import *
from telemeta.forms.haystack_form import *

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

    def __call__(self, request, type=None):
        self.type = type
        """if(self.type == 'collection'):
            self.form_class = HayAdvanceFormCollection
        else:
            self.form_class = HayAdvanceFormItem"""
        self.form_class = HayAdvanceForm
        return super(HaystackAdvanceSearch, self).__call__(request)

    def get_results(self):
        if(self.type == 'collection'):
            return self.form.search().models(MediaCollection)
        else:
            return self.form.search().models(MediaItem)

    def extra_context(self):
        extra = super(HaystackAdvanceSearch, self).extra_context()

        if self.request.GET.get('q'):
            extra['title'] = self.request.GET['q']

        if self.request.GET.get('cote'):
            extra['cote'] = self.request.GET['cote']

        if self.request.GET.get('location'):
            extra['location'] = self.request.GET['location']

        extra['collection_count'] = self.form.search().models(MediaCollection).count()
        extra['item_count'] = self.form.search().models(MediaItem).count()
        if self.type == 'collection':
            extra['type'] = 'collection'
        else:
            extra['type'] = 'item'
        return extra

# -*- coding: utf-8 -*-
from telemeta.models import *
from haystack.forms import *
from haystack.query import SearchQuerySet

class HaySearchForm(FacetedSearchForm):

    def search(self):
        sqs=SearchQuerySet().load_all()

        if not self.is_valid():
            return sqs

        if self.cleaned_data['q']:
            sqs=sqs.filter(content__contains=self.cleaned_data['q']).facet('item_acces').facet('item_status').facet('digitized')

        for facet in self.selected_facets:
            if ":" not in facet:
                continue

            field, value = facet.split(":", 1)

            if value:
                if value == 'viewable':
                    sqs = sqs.narrow('item_acces:full OR item_acces:mixed').narrow('digitized:T')
                else:
                    sqs = sqs.narrow(u'%s:"%s"' % (field, sqs.query.clean(value)))

        return sqs




class HayAdvanceFormItem(SearchForm):

    cote = forms.CharField(required=False, label=('Cote'), widget=forms.TextInput(attrs={'type': 'search'}))

    def search(self):
        sqs = super(HayAdvanceFormItem, self).search().models(MediaItem)

        if not self.is_valid():
            return sqs

        if self.cleaned_data['q']:
            sqs = sqs.filter(content__contains=self.cleaned_data['q'])

        if self.cleaned_data['cote']:
            sqs = sqs.filter(content__cote__contains=self.cleaned_data['cote'])

        return sqs


class HayAdvanceFormCollection(SearchForm):

    cote = forms.CharField(required=False, label=('Cote'), widget=forms.TextInput(attrs={'type': 'search'}))

    def search(self):
        sqs = super(HayAdvanceFormCollection, self).search().models(MediaCollection)

        if not self.is_valid():
            return sqs

        if self.cleaned_data['q']:
            sqs = sqs.filter(content__contains=self.cleaned_data['q'])

        if self.cleaned_data['cote']:
            sqs = sqs.filter(content__cote__contains=self.cleaned_data['cote'])

        return sqs


class HayAdvanceForm(SearchForm):
    #to replace de basic search form field
    q = forms.CharField(required=False, label=('Title'), widget=forms.TextInput(attrs={'type': 'search'}))
    code = forms.CharField(required=False, label=('Code'), widget=forms.TextInput(attrs={'type': 'search'}))
    location = forms.CharField(required=False, label=('Location'), widget=forms.TextInput(attrs={'type': 'search'}))

    def search(self):
        sqs = SearchQuerySet().load_all()

        if not self.is_valid():
            return self.no_query_found()

        if self.cleaned_data.get('q'):
            sqs = sqs.filter(title__title__contains=self.cleaned_data['q'])

        if self.cleaned_data.get('code'):
            sqs = sqs.filter(code__code__contains=self.cleaned_data['code'])

        if self.cleaned_data.get('location'):
            sqs = sqs.filter(location__location__contains=self.cleaned_data['location'])

        return sqs

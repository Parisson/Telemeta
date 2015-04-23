# -*- coding: utf-8 -*-
from django import forms
from telemeta.models import *
from haystack.inputs import AutoQuery, Exact, Clean
from haystack.forms import *
from haystack.query import SearchQuerySet

class HaySearchFormItem(SearchForm):

    def search(self):
        sqs=SearchQuerySet().load_all()

        if not self.is_valid():
            return sqs

        if self.cleaned_data['q']:
            sqs=sqs.models(MediaItem).filter(content__contains=self.cleaned_data['q'])

        return sqs

class HaySearchFormCollection(SearchForm):

    def search(self):
        sqs=SearchQuerySet().load_all()

        if not self.is_valid():
            return sqs

        if self.cleaned_data['q']:
            sqs=sqs.models(MediaCollection).filter(content__contains=self.cleaned_data['q'])

        return sqs


# -*- coding: utf-8 -*-
from django import forms
from haystack.inputs import AutoQuery, Exact, Clean
from haystack.forms import SearchForm
from haystack.query import SearchQuerySet

class HaySearchForm(SearchForm):

    def search(self):
        sqs=SearchQuerySet().load_all()

        if not self.is_valid():
            return sqs

        if self.cleaned_data['q']:
            sqs=sqs.filter(content__contains=self.cleaned_data['q'])

        return sqs


# -*- coding: utf-8 -*-

from haystack.views import SearchView
from haystack.query import SearchQuerySet

class HaystackSearch(SearchView):

    def get_query(self):
        query=super(HaystackSearch, self).get_query()
        return query





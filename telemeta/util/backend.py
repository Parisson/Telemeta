# -*- coding: utf-8 -*-

from haystack.backends.elasticsearch_backend import *

class CustomElasticBackend(ElasticsearchSearchBackend):

    def setup(self):

        DEFAULT_FIELD_MAPPING['analyzer']='space_lower_analyzer'
        eb = super(CustomElasticBackend, self)
        eb.DEFAULT_SETTINGS.get('settings').get('analysis').get('analyzer')['space_lower_analyzer']=\
            {"type": "custom", "tokenizer": "whitespace", "filter": ["lowercase", "asciifolding"]}
        eb.setup()

class CustomElasticSearchQuery(ElasticsearchSearchQuery):

    def build_query_fragment(self, field, filter_type, value):
        #print(field, ' ', filter_type, ' ', value)
        valeur = super(CustomElasticSearchQuery, self).build_query_fragment(field, filter_type, value)
        #print(valeur)
        return valeur

    def build_query(self):
        valeur = super(CustomElasticSearchQuery, self).build_query()
        print(valeur)
        return valeur

class CustomElasticEngine(ElasticsearchSearchEngine):
    backend = CustomElasticBackend
    query = CustomElasticSearchQuery


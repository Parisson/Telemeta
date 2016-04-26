# -*- coding: utf-8 -*-

from haystack.backends.elasticsearch_backend import *

class CustomElasticBackend(ElasticsearchSearchBackend):

    def setup(self):
        DEFAULT_FIELD_MAPPING['analyzer']='snowball_asciifolding_analyzer'
        eb = super(CustomElasticBackend, self)
        eb.DEFAULT_SETTINGS.get('settings').get('analysis').get('analyzer')['snowball_asciifolding_analyzer']=\
            {"type": "custom", "tokenizer": "letter", "filter": ["lowercase", "stop",  "asciifolding"]}
        eb.setup()


import unicodedata
class CustomElasticSearchQuery(ElasticsearchSearchQuery):

    def build_query_fragment(self, field, filter_type, value):
        #print(field, ' ', filter_type, ' ', value)
        valeur = super(CustomElasticSearchQuery, self).build_query_fragment(field, filter_type, value)
        #print(valeur)
        return valeur

    def build_query(self):
        valeur = super(CustomElasticSearchQuery, self).build_query()
        print (unicodedata.normalize('NFD', valeur).encode('ascii', 'ignore'))
        return valeur

class CustomElasticEngine(ElasticsearchSearchEngine):
    backend = CustomElasticBackend
    query = CustomElasticSearchQuery


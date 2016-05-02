# -*- coding: utf-8 -*-

from haystack.backends.elasticsearch_backend import *
import string
import re

regexSpacePunc = "[\\s"+re.escape(string.punctuation)+"]+"

class CustomElasticBackend(ElasticsearchSearchBackend):

    def setup(self):
        DEFAULT_FIELD_MAPPING['analyzer']='whitespace_asciifolding_analyzer'
        FIELD_MAPPINGS['keyword'] = {'type': 'string', 'analyzer':'lowercase_analyzer'}
        eb = super(CustomElasticBackend, self)
        eb.DEFAULT_SETTINGS.get('settings').get('analysis').get('tokenizer')['esc_scape_tokenizer']=\
            {"type": "pattern", "pattern": regexSpacePunc}
        eb.DEFAULT_SETTINGS.get('settings').get('analysis').get('analyzer')['whitespace_asciifolding_analyzer']=\
            {"type": "custom", "tokenizer": "esc_scape_tokenizer", "filter": ["lowercase", "asciifolding"]}
        eb.DEFAULT_SETTINGS.get('settings').get('analysis').get('analyzer')['lowercase_analyzer'] = \
            {"type": "custom", "tokenizer": "keyword", "filter": ["lowercase"]}
        eb.setup()


import unicodedata
import sys
class CustomElasticSearchQuery(ElasticsearchSearchQuery):

    def build_query_fragment(self, field, filter_type, value):
        value = re.sub(regexSpacePunc, " ", str(value))
        print("Query fragment :"+ field+ ' '+ filter_type+ ' '+ value)
        sys.stdout.flush()
        valeur = super(CustomElasticSearchQuery, self).build_query_fragment(field, filter_type, value)
        print("Query fragment result "+ valeur)
        sys.stdout.flush()
        return valeur

    def build_query(self):
        valeur = super(CustomElasticSearchQuery, self).build_query()
        print (unicodedata.normalize('NFD', valeur).encode('ascii', 'ignore'))
        return valeur

class CustomElasticEngine(ElasticsearchSearchEngine):
    backend = CustomElasticBackend
    query = CustomElasticSearchQuery


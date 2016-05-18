# -*- coding: utf-8 -*-

from haystack.backends.elasticsearch_backend import *
import string
import re

#Regex for remove punctuations when index fields and
#when submit a query search
regex_space_punc = "[\\s" + re.escape(string.punctuation) + "]+"

class CustomElasticBackend(ElasticsearchSearchBackend):

    #This setup modifies the mapping of ES in order to have better results
    #in the search engine. Add 2 analyzers (for indexing and searching):
    # -whitespace_asciifolding_analyzer : remove punctuations and convert
    #  all terms into lowercase and escape accents.
    # -lowercase_analyzer : convert in lowercase the word (used by code field
    #  in order to preserve undersore of codes)

    def setup(self):
        DEFAULT_FIELD_MAPPING['analyzer']='whitespace_asciifolding_analyzer'
        FIELD_MAPPINGS['keyword'] = {'type': 'string', 'analyzer':'lowercase_analyzer'}
        eb = super(CustomElasticBackend, self)
        eb.DEFAULT_SETTINGS.get('settings').get('analysis').get('tokenizer')['esc_scape_tokenizer']=\
            {"type": "pattern", "pattern": regex_space_punc}
        eb.DEFAULT_SETTINGS.get('settings').get('analysis').get('analyzer')['whitespace_asciifolding_analyzer']=\
            {"type": "custom", "tokenizer": "esc_scape_tokenizer", "filter": ["lowercase", "asciifolding"]}
        eb.DEFAULT_SETTINGS.get('settings').get('analysis').get('analyzer')['lowercase_analyzer'] = \
            {"type": "custom", "tokenizer": "keyword", "filter": ["lowercase"]}
        eb.setup()

class CustomElasticSearchQuery(ElasticsearchSearchQuery):

    #Custom search query for remove all punctuations characters and
    #convert to string for boolean fields
    #Used when enter the query

    def build_query_fragment(self, field, filter_type, value):
        if isinstance(value, bool):
        	value = str(value)
    	if not isinstance(value, int) and field !='code':
        	value = re.sub(regex_space_punc, " ", value)
        valeur = super(CustomElasticSearchQuery, self).build_query_fragment(field, filter_type, value)
        return valeur

#The custom engine that determine backednd and search_query
class CustomElasticEngine(ElasticsearchSearchEngine):
    backend = CustomElasticBackend
    query = CustomElasticSearchQuery


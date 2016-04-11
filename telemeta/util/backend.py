from haystack.backends.elasticsearch_backend import *

class CustomElasticBackend(ElasticsearchSearchBackend):

    def setup(self):
    	FIELD_MAPPINGS.get('ngram')['search_analyzer']='startspacelower'
        eb = super(CustomElasticBackend, self)
        eb.DEFAULT_SETTINGS.get('settings').get('analysis').get('analyzer')['startspacelower']={"type":"pattern", "pattern":"^\\s+", "filter": ["lowercase"]}
        ngram = eb.DEFAULT_SETTINGS.get('settings').get('analysis').get('analyzer').get('ngram_analyzer')
        ngram['tokenizer']='keyword'
        ngram.get('filter').insert(0, 'trim')
        eb.setup()

class CustomElasticEngine(ElasticsearchSearchEngine):
    backend = CustomElasticBackend

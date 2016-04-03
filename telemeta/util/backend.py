from haystack.backends.elasticsearch_backend import *

class CustomElasticBackend(ElasticsearchSearchBackend):

    def setup(self):
        FIELD_MAPPINGS.get('edge_ngram')['search_analyzer']="standard";
        FIELD_MAPPINGS.get('ngram')['search_analyzer']="standard";
        eb = super(CustomElasticBackend, self)
        eb.DEFAULT_SETTINGS.get('settings').get('analysis').get('filter').get('haystack_ngram')['max_gram']=30
        eb.setup()

class CustomElasticEngine(ElasticsearchSearchEngine):
    backend = CustomElasticBackend
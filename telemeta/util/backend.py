from haystack.backends.elasticsearch_backend import *

class CustomElasticBackend(ElasticsearchSearchBackend):

    def setup(self):

        DEFAULT_FIELD_MAPPING['analyzer']='trim_lower_analyzer'
        FIELD_MAPPINGS['instrument']={'type':'string', 'analyzer':'pipe_analyzer', 'search_analyzer': 'trim_lower_analyzer'}
        eb = super(CustomElasticBackend, self)
        eb.DEFAULT_SETTINGS.get('settings').get('analysis').get('tokenizer')['pipe_tokenizer']=\
            {'type': 'pattern', 'pattern': '\\|'}
        eb.DEFAULT_SETTINGS.get('settings').get('analysis').get('analyzer')['trim_lower_analyzer']=\
            {"type": "custom", "tokenizer": "keyword", "filter": ["trim", "lowercase", "asciifolding"]}
        eb.DEFAULT_SETTINGS.get('settings').get('analysis').get('analyzer')['pipe_analyzer']=\
            {'type':'custom', 'tokenizer': 'pipe_tokenizer', 'filter': ['trim', 'lowercase', 'asciifolding']}
        eb.setup()

class CustomElasticEngine(ElasticsearchSearchEngine):
    backend = CustomElasticBackend

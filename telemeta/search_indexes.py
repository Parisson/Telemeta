from haystack import indexes
from telemeta.models import *


class MediaItemIndex(indexes.SearchIndex, indexes.Indexable):

    text = indexes.CharField(document=True, use_template=True)
    item_acces = indexes.CharField(model_attr= 'collection__public_access' , faceted=True)
    item_status = indexes.CharField(model_attr= 'collection__document_status' , faceted=True)
    title = indexes.NgramField(model_attr='title')
    code = indexes.NgramField(model_attr='code')
    location = indexes.NgramField(model_attr='location__name', default='')

    def get_model(self):
        return MediaItem


class MediaCollectionIndex(indexes.SearchIndex, indexes.Indexable):

    text = indexes.NgramField(document=True, use_template=True)
    #rec_date = indexes.DateTimeField(use_template=True, null=True)
    title = indexes.NgramField(model_attr='title')
    code = indexes.NgramField(model_attr='code')
    location = indexes.NgramField(default='')

    def get_model(self):
        return MediaCollection

    def prepare_location(self, obj):
        return "%s" % obj.countries()
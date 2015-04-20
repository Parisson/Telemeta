from haystack import indexes
from telemeta.models import *


class MediaItemIndex(indexes.SearchIndex, indexes.Indexable):

    text = indexes.NgramField(document=True, use_template=True)
    #rec_date = indexes.DateTimeField(use_template=True, null=True)

    def get_model(self):
        return MediaItem



from haystack import indexes
from telemeta.models import *


class MediaItemIndex(indexes.SearchIndex, indexes.Indexable):

    title = indexes.CharField(use_template=True, document=True)

    def get_model(self):
        return MediaItem

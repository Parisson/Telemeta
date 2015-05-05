from haystack import indexes
from telemeta.models import *


class MediaItemIndex(indexes.SearchIndex, indexes.Indexable):

    text = indexes.CharField(document=True, use_template=True)
    item_acces = indexes.CharField(model_attr='collection__public_access', faceted=True)
    item_status = indexes.CharField(model_attr='collection__document_status', faceted=True)
    digitized = indexes.BooleanField(default=False, faceted=True)
    media_type = indexes.CharField(model_attr='media_type', null='None', faceted=True)
    recording_context = indexes.CharField(model_attr='collection__recording_context', default='', faceted=True)
    #original_format = indexes.CharField(model_attr='collection__original_format', default='', faceted=True)
    physical_format = indexes.CharField(model_attr='collection__physical_format', default='', faceted=True)

    #advance search
    title = indexes.NgramField(model_attr='title')
    code = indexes.NgramField(model_attr='code')
    location = indexes.NgramField(model_attr='location__name', default='')
    ethnic_group = indexes.NgramField(model_attr='ethnic_group', default='')
    instruments = indexes.NgramField(default='')
    collectors = indexes.NgramField(model_attr='collector', default='')
    recorded_from_date = indexes.DateField(model_attr='recorded_from_date', null='None')
    recorded_to_date = indexes.DateField(model_attr='recorded_to_date', null='None')
    year_published = indexes.IntegerField(model_attr='collection__year_published', default='')

    def prepare_digitized(self, obj):
        if obj.file.name:
            return True
        elif '/' in obj.url:
            return True
        else:
            return False

    def get_model(self):
        return MediaItem

    def prepare_location(self, obj):
        location = []
        location.append(obj.location)
        location_alias = LocationAlias.objects.filter(location__name=obj.location)
        location_rela = LocationRelation.objects.filter(location__name=obj.location)
        for rela in location_rela:
            location.append(rela.ancestor_location)
        for alias in location_alias:
            location.append(alias)
        return "%s" % location

    def prepare_instruments(self, obj):
        item = MediaItemPerformance.objects.all().filter(media_item__title__contains=obj.title)
        instruments = []
        for material in item:
            instruments.append(material.instrument)
            instruments.append(material.alias)
        return "%s" % instruments

    def prepare_collectors(self, obj):
        collectors = []
        collectors.append(obj.collection.creator)
        collectors.append(obj.collection.collector)
        collectors.append(obj.collector)
        return "%s" % collectors


class MediaCollectionIndex(indexes.SearchIndex, indexes.Indexable):

    text = indexes.NgramField(document=True, use_template=True)
    #rec_date = indexes.DateTimeField(use_template=True, null=True)
    item_acces = indexes.CharField(model_attr='public_access', faceted=True)
    item_status = indexes.CharField(model_attr='document_status', faceted=True)
    digitized = indexes.BooleanField(default=False, faceted=True)
    media_type = indexes.CharField(model_attr='media_type', null='None', faceted=True)
    recording_context = indexes.CharField(model_attr='recording_context', default='' ,faceted=True)
    #original_format = indexes.CharField(model_attr='original_format', default='', faceted=True)
    physical_format = indexes.CharField(model_attr='physical_format', default='', faceted=True)

    #advance search
    title = indexes.NgramField(model_attr='title')
    code = indexes.NgramField(model_attr='code')
    location = indexes.NgramField(default='')
    ethnic_group = indexes.NgramField(default='')
    instruments = indexes.NgramField(default='')
    collectors = indexes.NgramField(default='')
    recorded_from_date = indexes.DateField(model_attr='recorded_from_year', null='None')
    recorded_to_date = indexes.DateField(model_attr='recorded_to_year', null='None')
    year_published = indexes.IntegerField(model_attr='year_published', default='')

    def prepare_digitized(self, obj):
        return obj.has_mediafile

    def get_model(self):
        return MediaCollection

    def prepare_location(self, obj):
        collec_location = []
        for item in obj.items.all():
            location = []
            location.append(item.location)
            location_alias = LocationAlias.objects.filter(location__name=item.location)
            location_rela = LocationRelation.objects.filter(location__name=item.location)
            for rela in location_rela:
                location.append(rela.ancestor_location)
            for alias in location_alias:
                location.append(alias)
            for name in location:
                if name and not name in collec_location:
                    collec_location.append(name)
        return "%s" % collec_location

    def prepare_ethnic_group(self, obj):
        return "%s" % obj.ethnic_groups()

    def prepare_instruments(self, obj):
        instruments = []
        items = obj.items.all()
        for item in items:
            materials = MediaItemPerformance.objects.all().filter(media_item__title__exact=item.title)
            for material in materials:
                if material.instrument and not material.instrument in instruments:
                    instruments.append(material.instrument)

                if material.alias and not material.alias in instruments:
                    instruments.append(material.alias)

        return "%s" % instruments

    def prepare_collectors(self, obj):
        collectors = []
        collectors.append(obj.creator)
        collectors.append(obj.collector)
        return "%s" % collectors

# -*- coding: utf-8 -*-

# Copyright (C) 2015 Angy Fils-Aimé, Killian Mary

# This file is part of Telemeta.

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from haystack import indexes
from telemeta.models import *
from haystack.query import SearchQuerySet

class KeywordField(indexes.CharField):
    field_type = 'keyword'

class MediaItemIndex(indexes.SearchIndex, indexes.Indexable):

    text = indexes.CharField(document=True, use_template=True)
    item_acces = indexes.CharField(model_attr='collection__public_access', faceted=True)
    item_status = indexes.CharField(model_attr='collection__document_status', faceted=True)
    digitized = indexes.BooleanField(default=False, faceted=True)
    media_type = indexes.CharField(model_attr='media_type', null='None', faceted=True)
    recording_context = indexes.CharField(model_attr='collection__recording_context', default='', faceted=True)
    physical_format = indexes.CharField(model_attr='collection__physical_format', default='', faceted=True)
    #content_auto = indexes.EdgeNgramField(model_attr='content')

    #advance search
    title = indexes.CharField(model_attr='title')
    code = KeywordField(model_attr='code', default='')
    location_principal = indexes.CharField(null='None', boost=1.05)
    location_relation = indexes.CharField()
    ethnic_group = indexes.CharField(model_attr='ethnic_group', default='')
    instruments = indexes.CharField(default='')
    collectors = indexes.CharField(model_attr='collector', default='')
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

    def prepare_location_principal(self, obj):
        if obj.location is not None:
            return u"".join(obj.location.name)
        else:
            return None

    def prepare_location_relation(self, obj):
        location = []
        if obj.location is not None:
            location_alias = LocationAlias.objects.filter(location__name=obj.location)
            location_rela = LocationRelation.objects.filter(location__name=obj.location)
            for rela in location_rela:
                location.append(rela.ancestor_location.name)
            for alias in location_alias:
                location.append(alias.alias)
            if obj.location.current_location is not None:
                location.append(obj.location.current_location.name)
            #print u"".join(' ' + local for local in location).encode("utf-8")
            #print u"%s".encode("utf-8") % location
            #print [local for local in location]
        return u"".join('|' + local for local in location)

    def prepare_instruments(self, obj):
        item = MediaItemPerformance.objects.all().filter(media_item__exact=obj)
        instruments = []
        for material in item:
            if material.instrument is not None:
                instruments.append(material.instrument.name)
            if material.alias is not None:
                instruments.append(material.alias.name)
        return u"".join('|' + instru for instru in instruments)

    def prepare_collectors(self, obj):
        collectors = []
        collectors.append(obj.collection.collector)
        collectors.append(obj.collector)
        return u"".join('; ' + collector for collector in collectors)


class MediaCollectionIndex(indexes.SearchIndex, indexes.Indexable):

    text = indexes.CharField(document=True, use_template=True)
    item_acces = indexes.CharField(model_attr='public_access', faceted=True)
    item_status = indexes.CharField(model_attr='document_status', faceted=True)
    digitized = indexes.BooleanField(default=False, faceted=True)
    media_type = indexes.CharField(model_attr='media_type', null='None', faceted=True)
    recording_context = indexes.CharField(model_attr='recording_context', default='', faceted=True)
    physical_format = indexes.CharField(model_attr='physical_format', default='', faceted=True)
    #content_auto = indexes.EdgeNgramField(model_attr='content')

    #advance search
    title = indexes.CharField(model_attr='title')
    code = KeywordField(model_attr='code', default='')
    location_principal = indexes.CharField(default='', boost=1.05)
    location_relation = indexes.CharField()
    ethnic_group = indexes.CharField(default='')
    instruments = indexes.CharField(default='')
    collectors = indexes.CharField(model_attr='collector', default='')
    recorded_from_date = indexes.DateField(model_attr='recorded_from_year', null=True)
    recorded_to_date = indexes.DateField(model_attr='recorded_to_year', null=True)
    year_published = indexes.IntegerField(model_attr='year_published', default='')

    def prepare_digitized(self, obj):
        return obj.has_mediafile

    def get_model(self):
        return MediaCollection

    def prepare_location_principal(self, obj):
        collec_location = []
        for item in obj.items.all():
            location = []
            if item.location is not None:
                collec_location.append(item.location.name)
        return u"".join('|' + location for location in collec_location)

    def prepare_location_relation(self, obj):
        collec_location = []
        for item in obj.items.all():
            location = []
            if item.location is not None:
                location_alias = LocationAlias.objects.filter(location__name=item.location)
                location_rela = LocationRelation.objects.filter(location__name=item.location)
                for rela in location_rela:
                    location.append(rela.ancestor_location.name)
                for alias in location_alias:
                    location.append(alias.alias)
                if item.location.current_location is not None:
                    location.append(item.location.current_location.name)
                for name in location:
                    if name and not name in collec_location:
                        collec_location.append(name)
        return u"".join('|' + location for location in collec_location)

    def prepare_ethnic_group(self, obj):
        return "%s" % obj.ethnic_groups()

    def prepare_instruments(self, obj):
        instruments = []
        items = obj.items.all()
        for item in items:
            materials = MediaItemPerformance.objects.all().filter(media_item__exact=item)
            for material in materials:
                if material.instrument and not material.instrument in instruments:
                    instruments.append(material.instrument.name)

                if material.alias and not material.alias in instruments:
                    instruments.append(material.alias.name)
        return u"".join('|' + instru for instru in instruments)

    def prepare_recorded_from_date(self, obj):
        if obj.recorded_from_year != 0:
            return datetime.date(int(obj.recorded_from_year), 01, 01)
        else:
            return None

    def prepare_recorded_to_date(self, obj):
        if obj.recorded_to_year != 0:
            return datetime.date(int(obj.recorded_to_year), 01, 01)
        else:
            return None


class MediaCorpusIndex(indexes.SearchIndex, indexes.Indexable):

    text = indexes.CharField(document=True, use_template=True)
    #item_acces = indexes.CharField(model_attr='public_access', faceted=True)
    #item_status = indexes.CharField(model_attr='document_status', faceted=True)
    digitized = indexes.BooleanField(default=False, faceted=True)
    #media_type = indexes.CharField(model_attr='media_type', null='None', faceted=True)
    #recording_context = indexes.CharField(model_attr='recording_context', default='', faceted=True)
    #physical_format = indexes.CharField(model_attr='collection__physical_format', default='', faceted=True)
    #content_auto = indexes.EdgeNgramField(model_attr='content')

    #advance search
    title = indexes.CharField(model_attr='title')
    code = KeywordField(model_attr='code', default='')
    #location_principal = indexes.CharField(default='', boost=1.05)
    #location_relation = indexes.CharField()
    #ethnic_group = indexes.CharField(default='')
    #instruments = indexes.NgramField(default='')
    #collectors = indexes.NgramField(model_attr='collector', default='')
    #recorded_from_date = indexes.DateField(model_attr='recorded_from_year', null=True)
    recorded_to_date = indexes.DateField(model_attr='recorded_to_year', null=True)
    #year_published = indexes.IntegerField(model_attr='year_published', default='')

    def prepare_digitized(self, obj):
        return obj.has_mediafile

    def get_model(self):
        return MediaCorpus


class MediaFondsIndex(indexes.SearchIndex, indexes.Indexable):

    text = indexes.CharField(document=True, use_template=True)
    #item_acces = indexes.CharField(model_attr='public_access', faceted=True)
    #item_status = indexes.CharField(model_attr='document_status', faceted=True)
    digitized = indexes.BooleanField(default=False, faceted=True)
    #media_type = indexes.CharField(model_attr='media_type', null='None', faceted=True)
    #recording_context = indexes.CharField(model_attr='recording_context', default='', faceted=True)
    #physical_format = indexes.CharField(model_attr='physical_format', default='', faceted=True)
    #content_auto = indexes.EdgeNgramField(model_attr='content')

    #advance search
    title = indexes.CharField(model_attr='title')
    code = KeywordField(model_attr='code', default='')
    #location_principal = indexes.CharField(default='', boost=1.05)
    #location_relation = indexes.CharField()
    #ethnic_group = indexes.CharField(default='')
    #instruments = indexes.NgramField(default='')
    #collectors = indexes.NgramField(model_attr='collector', default='')
    #recorded_from_date = indexes.DateField(model_attr='recorded_from_year', null=True)
    #recorded_to_date = indexes.DateField(model_attr='recorded_to_year', null=True)
    #year_published = indexes.IntegerField(model_attr='year_published', default='')

    def prepare_digitized(self, obj):
        return obj.has_mediafile

    def get_model(self):
        return MediaFonds

class LocationIndex(indexes.SearchIndex, indexes.Indexable):

    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return Location

    def index_queryset(self, using=None):
        loc = MediaItem.objects.values('location')
        old = Location.objects.filter(current_location__in=loc).values('id')
        anc = LocationRelation.objects.filter(location__in=loc).values('ancestor_location')
        return Location.objects.filter(Q(pk__in=loc)|Q(pk__in=old)|Q(pk__in=anc))

class LocationAliasIndex(indexes.SearchIndex, indexes.Indexable):

    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return LocationAlias

    def index_queryset(self, using=None):
        l = MediaItem.objects.values('location')
        return LocationAlias.objects.filter(location__in=l)


class InstrumentIndex(indexes.SearchIndex, indexes.Indexable):

    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return Instrument

    def index_queryset(self, using=None):
        instrus = MediaItemPerformance.objects.values('instrument')
        return Instrument.objects.filter(pk__in=instrus)


class InstrumentAliasIndex(indexes.SearchIndex, indexes.Indexable):

    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return InstrumentAlias

    def index_queryset(self, using=None):
        instrualias = MediaItemPerformance.objects.values('alias')
        return InstrumentAlias.objects.filter(pk__in=instrualias)
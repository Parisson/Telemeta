# -*- coding: utf-8 -*-
# Copyright (C) 2007-2010 Samalyse SARL
# Copyright (C) 2010-2011 Parisson SARL
#
# This software is a computer program whose purpose is to backup, analyse,
# transcode and stream any audio content with its metadata over a web frontend.
#
# This software is governed by the CeCILL  license under French law and
# abiding by the rules of distribution of free software.  You can  use,
# modify and/ or redistribute the software under the terms of the CeCILL
# license as circulated by CEA, CNRS and INRIA at the following URL
# "http://www.cecill.info".
#
# As a counterpart to the access to the source code and  rights to copy,
# modify and redistribute granted by the license, users are provided only
# with a limited warranty  and the software's author,  the holder of the
# economic rights,  and the successive licensors  have only  limited
# liability.
#
# In this respect, the user's attention is drawn to the risks associated
# with loading,  using,  modifying and/or developing or reproducing the
# software by the user in light of its specific status of free software,
# that may mean  that it is complicated to manipulate,  and  that  also
# therefore means  that it is reserved for developers  and  experienced
# professionals having in-depth computer knowledge. Users are therefore
# encouraged to load and test the software's suitability as regards their
# requirements in conditions enabling the security of their systems and/or
# data to be ensured and,  more generally, to use and operate it in the
# same conditions as regards security.
#
# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL license and that you accept its terms.
#
# Authors: Olivier Guilyardi <olivier@samalyse.com>
#          David LIPSZYC <davidlipszyc@gmail.com>
#          Guillaume Pellerin <yomguy@parisson.com>

from django.conf import settings
from django.db.models import Q, Max, Min
from telemeta.models.core import *
from telemeta.util.unaccent import unaccent, unaccent_icmp
from telemeta.models.enum import EthnicGroup
import re

engine = settings.DATABASES['default']['ENGINE']

class MediaItemQuerySet(CoreQuerySet):
    "Base class for all media item query sets"

    def quick_search(self, pattern):
        "Perform a quick search on code, title and collector name"
        pattern = pattern.strip()

#        from telemeta.models.media import MediaItem
#        mod = MediaItem()
#        fields = mod.to_dict()
#        keys =  fields.keys()
#        q = self.by_fuzzy_collector_q(pattern)
#        for field in keys:
#            field_str = str(mod._meta.get_field(field))
#            if 'CharField' in field_str:
#                q = q | word_search_q(field)

        q = ( Q(code__contains=pattern) |
            Q(old_code__contains=pattern) |
            word_search_q('title', pattern) |
            word_search_q('comment', pattern) |
            self.by_fuzzy_collector_q(pattern) )

        return self.filter(q)

    def without_collection(self):
        "Find items which do not belong to any collection"
        return self.extra(
            where = ["collection_id NOT IN (SELECT id FROM media_collections)"]);

    def by_public_id(self, public_id):
        "Find items by public_id"
        return self.filter(public_id=public_id)

    def by_recording_date(self, from_date, to_date = None):
        "Find items by recording date"
        if to_date is None:
            return (self.filter(recorded_from_date__lte=from_date, recorded_to_date__gte=from_date))
        else :
            return (self.filter(Q(recorded_from_date__range=(from_date, to_date))
                                | Q(recorded_to_date__range=(from_date, to_date))))

    def by_title(self, pattern):
        "Find items by title"
        # to (sort of) sync with models.media.MediaItem.get_title()
        return self.filter(word_search_q("title", pattern) |
                           (Q(title="") & word_search_q("collection__title", pattern)))

    def by_publish_year(self, from_year, to_year = None):
        "Find items by publishing year"
        if to_year is None:
            to_year = from_year
        return self.filter(collection__year_published__range=(from_year, to_year))

    def by_change_time(self, from_time = None, until_time = None):
        "Find items by last change time"
        return self._by_change_time('item', from_time, until_time)

    def by_location(self, location):
        "Find items by location"
        return self.filter(location__in=location.apparented())

    @staticmethod
    def __name_cmp(obj1, obj2):
        return unaccent_icmp(obj1.name, obj2.name)

    def locations(self):
        from telemeta.models import Location, LocationRelation
        l = self.values('location')
        c = self.values('location__current_location')
        r = LocationRelation.objects.filter(location__in=l).values('ancestor_location')
        return Location.objects.filter(Q(pk__in=l) | Q(pk__in=r) | Q(pk__in=c))

    def countries(self, group_by_continent=False):
        countries = []
        from telemeta.models import Location
        for id in self.filter(location__isnull=False).values_list('location', flat=True).distinct():
            location = Location.objects.get(pk=id)
            for l in location.countries():
                c = l.current_location
                if not c in countries:
                    countries.append(c)

        if group_by_continent:
            grouped = {}

            for country in countries:
                for continent in country.continents():
                    if not grouped.has_key(continent):
                        grouped[continent] = []

                    grouped[continent].append(country)

            keys = grouped.keys()
            keys.sort(self.__name_cmp)
            ordered = []
            for c in keys:
                grouped[c].sort(self.__name_cmp)
                ordered.append({'continent': c, 'countries': grouped[c]})

            countries = ordered
        else:
            countries.sort(self.__name_cmp)

        return countries

    def virtual(self, *args):
        qs = self
        need_collection = False
        related = []
        from telemeta.models import Location
        for f in args:
            if f == 'apparent_collector':
                if not 'sqlite3' in engine:
                    related.append('collection')
                    qs = qs.extra(select={f:
                        'IF(collector_from_collection, '
                            'IF(media_collections.collector_is_creator, '
                               'media_collections.creator, '
                               'media_collections.collector),'
                            'media_items.collector)'})
            elif f == 'country_or_continent':
                related.append('location')
                if not 'sqlite3' in engine:
                    qs = qs.extra(select={f:
                        'IF(locations.type = ' + str(Location.COUNTRY) + ' '
                        'OR locations.type = ' + str(Location.CONTINENT) + ','
                        'locations.name, '
                        '(SELECT l2.name FROM location_relations AS r INNER JOIN locations AS l2 '
                        'ON r.ancestor_location_id = l2.id '
                        'WHERE r.location_id = media_items.location_id AND l2.type = ' + str(Location.COUNTRY) + ' LIMIT 1))'
                    })
            else:
                raise Exception("Unsupported virtual field: %s" % f)

        if related:
            qs = qs.select_related(*related)

        return qs

    def ethnic_groups(self):
        ids = self.filter(ethnic_group__isnull=False).values('ethnic_group');
        return EthnicGroup.objects.filter(pk__in=ids)

    @staticmethod
    def by_fuzzy_collector_q(pattern):
        return (word_search_q('collection__creator', pattern) |
                word_search_q('collection__collector', pattern) |
                word_search_q('collector', pattern))

    def by_fuzzy_collector(self, pattern):
        return self.filter(self.by_fuzzy_collector_q(pattern))

    def sound(self):
        return self.filter(file__contains='/')


class MediaItemManager(CoreManager):
    "Manage media items queries"

    def get_query_set(self):
        "Return media query sets"
        return MediaItemQuerySet(self.model)

    def enriched(self):
        "Query set with additional virtual fields such as apparent_collector and country_or_continent"
        return self.get_query_set().virtual('apparent_collector', 'country_or_continent')

    def quick_search(self, *args, **kwargs):
        return self.get_query_set().quick_search(*args, **kwargs)
    quick_search.__doc__ = MediaItemQuerySet.quick_search.__doc__

    def without_collection(self, *args, **kwargs):
        return self.get_query_set().without_collection(*args, **kwargs)
    without_collection.__doc__ = MediaItemQuerySet.without_collection.__doc__

    def by_recording_date(self, *args, **kwargs):
        return self.get_query_set().by_recording_date(*args, **kwargs)
    by_recording_date.__doc__ = MediaItemQuerySet.by_recording_date.__doc__

    def by_title(self, *args, **kwargs):
        return self.get_query_set().by_title(*args, **kwargs)
    by_title.__doc__ = MediaItemQuerySet.by_title.__doc__

    def by_publish_year(self, *args, **kwargs):
        return self.get_query_set().by_publish_year(*args, **kwargs)
    by_publish_year.__doc__ = MediaItemQuerySet.by_publish_year.__doc__

    def by_change_time(self, *args, **kwargs):
        return self.get_query_set().by_change_time(*args, **kwargs)
    by_change_time.__doc__ = MediaItemQuerySet.by_change_time.__doc__

    def by_location(self, *args, **kwargs):
        return self.get_query_set().by_location(*args, **kwargs)
    by_location.__doc__ = MediaItemQuerySet.by_location.__doc__

    def sound(self, *args, **kwargs):
        return self.get_query_set().sound(*args, **kwargs)
    sound.__doc__ = MediaItemQuerySet.sound.__doc__


class MediaCollectionQuerySet(CoreQuerySet):

    def quick_search(self, pattern):
        "Perform a quick search on code, title and collector name"
        from telemeta.models.media import MediaCollection
        pattern = pattern.strip()
        mod = MediaCollection()
        fields = mod.to_dict()
        keys =  fields.keys()
        q = self.by_fuzzy_collector_q(pattern)
        for field in keys:
            field_str = str(mod._meta.get_field(field))
            if 'CharField' in field_str or 'TextField' in field_str:
                q = q | word_search_q(field, pattern)
        return self.filter(q)

    def by_location(self, location):
        "Find collections by location"
        return self.filter(items__location__in=location.apparented()).distinct()

    def by_recording_year(self, from_year, to_year=None):
        "Find collections by recording year"
        if to_year is None:
            return (self.filter(recorded_from_year__lte=from_year, recorded_to_year__gte=from_year))
        else:
            return (self.filter(Q(recorded_from_year__range=(from_year, to_year)) |
                    Q(recorded_to_year__range=(from_year, to_year))))

    def by_publish_year(self, from_year, to_year=None):
        "Find collections by publishing year"
        if to_year is None:
            to_year = from_year
        return self.filter(year_published__range=(from_year, to_year))

    def by_ethnic_group(self, group):
        "Find collections by ethnic group"
        return self.filter(items__ethnic_group=group).distinct()

    def by_change_time(self, from_time=None, until_time=None):
        "Find collections between two dates"
        return self._by_change_time('collection', from_time, until_time)

    def virtual(self, *args):
        qs = self
        for f in args:
            if f == 'apparent_collector':
                if not 'sqlite3' in engine:
                    qs = qs.extra(select={f: 'IF(media_collections.collector_is_creator, '
                                         'media_collections.creator, media_collections.collector)'})
            else:
                raise Exception("Unsupported virtual field: %s" % f)

        return qs

    def recording_year_range(self):
        from_max = self.aggregate(Max('recorded_from_year'))['recorded_from_year__max']
        to_max   = self.aggregate(Max('recorded_to_year'))['recorded_to_year__max']
        year_max = max(from_max, to_max)

        from_min = self.filter(recorded_from_year__gt=0).aggregate(Min('recorded_from_year'))['recorded_from_year__min']
        to_min   = self.filter(recorded_to_year__gt=0).aggregate(Min('recorded_to_year'))['recorded_to_year__min']
        year_min = min(from_min, to_min)

        if not year_max:
            year_max = year_min
        elif not year_min:
            year_min = year_max

        return year_min, year_max

    def publishing_year_range(self):
        year_max = self.aggregate(Max('year_published'))['year_published__max']
        year_min = self.filter(year_published__gt=0).aggregate(Min('year_published'))['year_published__min']

        return year_min, year_max

    @staticmethod
    def by_fuzzy_collector_q(pattern):
        return word_search_q('creator', pattern) | word_search_q('collector', pattern)

    def by_fuzzy_collector(self, pattern):
        return self.filter(self.by_fuzzy_collector_q(pattern))

    def sound(self):
        return self.filter(items__file__contains='/').distinct()


class MediaCollectionManager(CoreManager):
    "Manage collection queries"

    def get_query_set(self):
        "Return the collection query"
        return MediaCollectionQuerySet(self.model)

    def enriched(self):
        "Query set with additional virtual fields such as apparent_collector"
        return self.get_query_set().virtual('apparent_collector')

    def quick_search(self, *args, **kwargs):
        return self.get_query_set().quick_search(*args, **kwargs)
    quick_search.__doc__ = MediaCollectionQuerySet.quick_search.__doc__

    def by_location(self, *args, **kwargs):
        return self.get_query_set().by_location(*args, **kwargs)
    by_location.__doc__ = MediaCollectionQuerySet.by_location.__doc__

    def by_recording_year(self, *args, **kwargs):
        return self.get_query_set().by_recording_year(*args, **kwargs)
    by_recording_year.__doc__ = MediaCollectionQuerySet.by_recording_year.__doc__

    def by_publish_year(self, *args, **kwargs):
        return self.get_query_set().by_publish_year(*args, **kwargs)
    by_publish_year.__doc__ = MediaCollectionQuerySet.by_publish_year.__doc__

    def by_ethnic_group(self, *args, **kwargs):
        return self.get_query_set().by_ethnic_group(*args, **kwargs)
    by_ethnic_group.__doc__ = MediaCollectionQuerySet.by_ethnic_group.__doc__

    def by_change_time(self, *args, **kwargs):
        return self.get_query_set().by_change_time(*args, **kwargs)
    by_change_time.__doc__ = MediaCollectionQuerySet.by_change_time.__doc__

    @staticmethod
    def __name_cmp(obj1, obj2):
        return unaccent_icmp(obj1.name, obj2.name)

    def sound(self, *args, **kwargs):
        return self.get_query_set().sound(*args, **kwargs)
    sound.__doc__ = MediaCollectionQuerySet.sound.__doc__


class LocationQuerySet(CoreQuerySet):
    __flatname_map = None

    def by_flatname(self, flatname):
        map = self.flatname_map()
        return self.filter(pk=map[flatname])

    def flatname_map(self):
        if self.__class__.__flatname_map:
            return self.__class__.__flatname_map

        map = {}
        locations = self.filter(Q(type=self.model.COUNTRY) | Q(type=self.model.CONTINENT))
        for l in locations:
            flatname = unaccent(l.name).lower()
            flatname = re.sub('[^a-z]', '_', flatname)
            while map.has_key(flatname):
                flatname = '_' + flatname
            map[flatname] = l.id

        self.__class__.__flatname_map = map
        return map

    def current(self):
        return self.filter(id__in=self.values_list('current_location_id', flat=True)).distinct()

class LocationManager(CoreManager):

    def get_query_set(self):
        "Return location query set"
        return LocationQuerySet(self.model)

    def by_flatname(self, *args, **kwargs):
        return self.get_query_set().by_flatname(*args, **kwargs)
    by_flatname.__doc__ = LocationQuerySet.by_flatname.__doc__

    def flatname_map(self, *args, **kwargs):
        return self.get_query_set().flatname_map(*args, **kwargs)
    flatname_map.__doc__ = LocationQuerySet.flatname_map.__doc__


class MediaCorpusQuerySet(CoreQuerySet):
    "Base class for all media resource query sets"

    def quick_search(self, pattern):
        "Perform a quick search on text and char fields"
        from telemeta.models.media import MediaCorpus
        mod = MediaCorpus()
        pattern = pattern.strip()
        q = Q(code__contains=pattern)
        fields = mod.to_dict()
        keys =  fields.keys()

        for field in keys:
            field_str = str(mod._meta.get_field(field))
            if 'CharField' in field_str or 'TextField' in field_str:
                q = q | word_search_q(field, pattern)

        return self.filter(q)


class MediaCorpusManager(CoreManager):
    "Manage media resource queries"

    def get_query_set(self):
        "Return resource query sets"
        return MediaCorpusQuerySet(self.model)

    def quick_search(self, *args, **kwargs):
        return self.get_query_set().quick_search(*args, **kwargs)
    quick_search.__doc__ = MediaCorpusQuerySet.quick_search.__doc__


class MediaFondsQuerySet(CoreQuerySet):
    "Base class for all media resource query sets"

    def quick_search(self, pattern):
        "Perform a quick search on text and char fields"
        from telemeta.models.media import MediaFonds
        mod = MediaFonds()
        pattern = pattern.strip()
        q = Q(code__contains=pattern)
        fields = mod.to_dict()
        keys =  fields.keys()
        for field in keys:
            field_str = str(mod._meta.get_field(field))
            if 'CharField' in field_str or 'TextField' in field_str:
                q = q | word_search_q(field, pattern)
        return self.filter(q)


class MediaFondsManager(CoreManager):
    "Manage media resource queries"

    def get_query_set(self):
        "Return resource query sets"
        return MediaFondsQuerySet(self.model)

    def quick_search(self, *args, **kwargs):
        return self.get_query_set().quick_search(*args, **kwargs)
    quick_search.__doc__ = MediaFondsQuerySet.quick_search.__doc__

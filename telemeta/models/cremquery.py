# -*- coding: utf-8 -*-
# Copyright (C) 2007 Samalyse SARL

# This software is a computer program whose purpose is to backup, analyse,
# transcode and stream any audio content with its metadata over a web frontend.

# This software is governed by the CeCILL  license under French law and
# abiding by the rules of distribution of free software.  You can  use,
# modify and/ or redistribute the software under the terms of the CeCILL
# license as circulated by CEA, CNRS and INRIA at the following URL
# "http://www.cecill.info".

# As a counterpart to the access to the source code and  rights to copy,
# modify and redistribute granted by the license, users are provided only
# with a limited warranty  and the software's author,  the holder of the
# economic rights,  and the successive licensors  have only  limited
# liability.

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

# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL license and that you accept its terms.
#
# Authors: Olivier Guilyardi <olivier@samalyse.com>
#          David LIPSZYC <davidlipszyc@gmail.com>

from django import db
from django.db.models import Manager, Q
from telemeta.models.core import EnhancedQuerySet, EnhancedManager
import re
from django.core.exceptions import ObjectDoesNotExist
from django import db
import _mysql_exceptions
from telemeta.util.unaccent import unaccent_icmp, unaccent

class CoreQuerySet(EnhancedQuerySet):
    "Base class for all query sets"

    def none(self): # redundant with none() in recent Django svn
        "Return an empty result set"
        return self.extra(where = ["0 = 1"])

    def word_search_q(self, field, pattern):
        words = re.split("[ .*-]+", pattern)
        q = Q()
        for w in words:
            if len(w) >= 3:
                kwargs = {field + '__icontains': w}
                q &= Q(**kwargs)

        return q

    def word_search(self, field, pattern):
        return self.filter(self.word_search_q(field, pattern))
        
    def _by_change_time(self, type, from_time = None, until_time = None):
        "Search between two revision dates"
        where = ["element_type = '%s'" % type]
        if from_time:
            where.append("time >= '%s'" % from_time.strftime('%Y-%m-%d %H:%M:%S'))
        if until_time:
            where.append("time <= '%s'" % until_time.strftime('%Y-%m-%d %H:%M:%S'))
        return self.extra(
            where = ["id IN (SELECT DISTINCT element_id FROM revisions WHERE %s)" % " AND ".join(where)]);

class CoreManager(EnhancedManager):
    "Base class for all models managers"

    def none(self, *args, **kwargs):
        ""
        return self.get_query_set().none(*args, **kwargs)

    def get(self, **kwargs):
        if kwargs.has_key('public_id'):
            try:
                args = kwargs.copy()
                args['code'] = kwargs['public_id']
                args.pop('public_id')
                return super(CoreManager, self).get(**args)
            except ObjectDoesNotExist:
                args = kwargs.copy()
                args['id'] = kwargs['public_id']
                args.pop('public_id')
                return super(CoreManager, self).get(**args)

        return super(CoreManager, self).get(**kwargs)
                
class MediaCollectionQuerySet(CoreQuerySet):

    def quick_search(self, pattern):
        "Perform a quick search on id, title and creator name"
        return self.filter(
            self.word_search_q('id', pattern) |
            self.word_search_q('title', pattern) |  
            self.word_search_q('creator', pattern)   
        )

    def by_location(self, location):
        "Find collections by country"
        return self.filter(Q(items__location=location) | Q(items__location__in=location.descendants())).distinct()
    
    def by_continent(self, continent):
        "Find collections by continent"
        return self.filter(items__location__type="continent", items__location=continent).distinct()

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
        return self.filter(items__ethnic_group__name=group).distinct()

    def by_change_time(self, from_time=None, until_time=None):
        "Find collections between two dates"
        return self._by_change_time('collection', from_time, until_time)

class MediaCollectionManager(CoreManager):
    "Manage collection queries"

    def get_query_set(self):
        "Return the collection query"
        return MediaCollectionQuerySet(self.model)

    def quick_search(self, *args, **kwargs):
        return self.get_query_set().quick_search(*args, **kwargs)
    quick_search.__doc__ = MediaCollectionQuerySet.quick_search.__doc__

    def by_location(self, *args, **kwargs):
        return self.get_query_set().by_location(*args, **kwargs)
    by_location.__doc__ = MediaCollectionQuerySet.by_location.__doc__

    def by_continent(self, *args, **kwargs):
        return self.get_query_set().by_continent(*args, **kwargs)
    by_continent.__doc__ = MediaCollectionQuerySet.by_continent.__doc__

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

    def stat_continents(self, only_continent=None):      
        "Return the number of collections by continents and countries as a tree"
        from telemeta.models import MediaItem, Location

        countries = []
        for lid in MediaItem.objects.filter(location__isnull=False).values_list('location', flat=True).distinct():
            location = Location.objects.get(pk=lid)
            if not only_continent or (only_continent in location.ancestors().filter(type=Location.CONTINENT)):
                for l in location.countries():
                    if not l in countries:
                        countries.append(l)
                
        stat = {}

        for country in countries:
            count = country.collections().count()
            for continent in country.ancestors().filter(type=Location.CONTINENT):
                if not stat.has_key(continent):
                    stat[continent] = {}

                stat[continent][country] = count
                
        keys1 = stat.keys()
        keys1.sort(self.__name_cmp)
        ordered = []
        for c in keys1:
            keys2 = stat[c].keys()
            keys2.sort(self.__name_cmp)
            sub = [{'location': d, 'count': stat[c][d]} for d in keys2]
            ordered.append({'location': c, 'countries': sub})
        
        return ordered


class MediaItemQuerySet(CoreQuerySet):
    "Base class for all media item query sets"
    
    def quick_search(self, pattern):
        "Perform a quick search on id and title"
        return self.filter(
            self.word_search_q('id', pattern) |
            self.word_search_q('title', pattern) |  
            self.word_search_q('author', pattern)   
        )

    def without_collection(self):        
        "Find items which do not belong to any collection"
        return self.extra(
            where = ["collection_id NOT IN (SELECT id FROM media_collections)"]);

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
        return self.filter(self.word_search_q("title", pattern) | self.word_search_q("collection__title", pattern))

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
        from telemeta.models import LocationRelation
        descendants = LocationRelation.objects.filter(ancestor_location=location)
        return self.filter(Q(location=location) | Q(location__in=descendants))
            
class MediaItemManager(CoreManager):
    "Manage media items queries"

    def get_query_set(self):
        "Return media query sets"
        return MediaItemQuerySet(self.model)

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

class LocationQuerySet(CoreQuerySet):
    def by_flatname(self, flatname):
        map = LocationManager.flatname_map()
        return self.filter(pk=map[flatname])

class LocationManager(CoreManager):
    __flatname_map = None

    def get_query_set(self):
        "Return location query set"
        return LocationQuerySet(self.model)

    @classmethod
    def flatname_map(cls):
        if cls.__flatname_map:
            return cls.__flatname_map

        from telemeta.models import Location
        map = {}
        locations = Location.objects.filter(Q(type=Location.COUNTRY) | Q(type=Location.CONTINENT))
        for l in locations:
            flatname = unaccent(l.name).lower()
            flatname = re.sub('[^a-z]', '_', flatname)
            while map.has_key(flatname):
                flatname = '_' + flatname
            map[flatname] = l.id

        cls.__flatname_map = map
        return map
            
    def by_flatname(self, *args, **kwargs):
        return self.get_query_set().by_flatname(*args, **kwargs)
    by_flatname.__doc__ = LocationQuerySet.by_flatname.__doc__    

    

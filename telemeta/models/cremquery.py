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
# Author: Olivier Guilyardi <olivier@samalyse.com>

from django.db.models import Manager, Q
from django.db.models.query import QuerySet

class CoreQuerySet(QuerySet):
    "Base class for all query sets"

    def none(self): # redundant with none() in recent Django svn
        "Return an empty result set"
        return self.extra(where = ["0 = 1"])

    def pattern_to_regex(self, pattern):
        "Cast a pattern into a regex with wildcards between words"
        regex = pattern;
        regex = regex.replace('*', '.*')
        regex = regex.replace('.', '.*')
        regex = regex.replace('-', '.*')
        regex = regex.replace(' ', '.*')
        return regex

    def word_search(self, field, pattern):
        "Look for words contained in the pattern in a specific field"
        regex = self.pattern_to_regex(pattern)
        kwargs = {field + '__iregex': regex}
        return self.filter(**kwargs)

    def _by_change_time(self, type, from_time = None, until_time = None):
        "Search between two revision dates"
        where = ["element_type = '%s'" % type]
        if from_time:
            where.append("time >= '%s'" % from_time.strftime('%Y-%m-%d %H:%M:%S'))
        if until_time:
            where.append("time <= '%s'" % until_time.strftime('%Y-%m-%d %H:%M:%S'))
        return self.extra(
            where = ["id IN (SELECT DISTINCT element_id FROM telemeta_revision WHERE %s)" % " AND ".join(where)]);

class CoreManager(Manager):
    "Base class for all models managers"

    def none(self, *args, **kwargs):
        ""
        return self.get_query_set().none(*args, **kwargs)

class MediaCollectionQuerySet(CoreQuerySet):

    def quick_search(self, pattern):
        "Perform a quick search on id, title and creator name"
        regex = self.pattern_to_regex(pattern)
        return self.filter(
            Q(id__iregex=regex) |
            Q(title__iregex=regex) |
            Q(creator__iregex=regex)
        )

    def by_country(self, country):
        "Find collections by country"
        return self.filter(items__location_name__type="country", items__location_name=country).distinct()
    
    def by_continent(self, continent):
        "Find collections by continent"
        return self.filter(items__location_name__type="continent", items__location_name=continent).distinct()

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

    def by_country(self, *args, **kwargs):
        return self.get_query_set().by_country(*args, **kwargs)
    by_country.__doc__ = MediaCollectionQuerySet.by_country.__doc__

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

    def stat_continents(self, order_by='num'):      
        "Return the number of collections by continents and countries as a tree"
        from django.db import connection
        cursor = connection.cursor()
        if order_by == 'num':
            order_by = 'items_num DESC'
        else:
            order_by = 'etat'
        cursor.execute("SELECT continent, etat, count(*) AS items_num "
            "FROM media_collections INNER JOIN media_items "
            "ON media_collections.id = media_items.collection_id "
            "WHERE (continent IN "
            "  ('EUROPE', 'OCEANIE', 'ASIE', 'AMERIQUE', 'AFRIQUE')) "
            "AND etat <> '' "
            "GROUP BY etat ORDER BY continent, " + order_by)
        result_set = cursor.fetchall()
        stat = {}
        for continent, country, count in result_set:
            if stat.has_key(continent):
                stat[continent].append({'name':country, 'count':count})
            else:
                stat[continent] = [{'name':country, 'count':count}]

        keys = stat.keys()
        keys.sort()
        ordered = [{'name': k, 'countries': stat[k]} for k in keys]
        return ordered

    def list_countries(self):
        "Return a 2D list of all countries with continents"

        from django.db import connection
        cursor = connection.cursor()

        cursor.execute("SELECT continent, etat FROM telemeta_item "
            "GROUP BY continent, etat ORDER BY REPLACE(etat, '\"', '')");
        return cursor.fetchall()

    def list_continents(self):
        "Return a list of all continents"
        
        from django.db import connection
        cursor = connection.cursor()

        cursor.execute("SELECT DISTINCT(name) FROM locations WHERE type = 'continent' ORDER BY name")
        result_set = cursor.fetchall()
        result = []
        for a, in result_set:
            if a != '' and a != 'N': # CREM fix
                result.append(a)
        
        return result

class MediaItemQuerySet(CoreQuerySet):
    "Base class for all media item query sets"
    
    def quick_search(self, pattern):
        "Perform a quick search on id and title"
        regex = self.pattern_to_regex(pattern)
        return self.filter(
            Q(id__iregex=regex) |
            Q(title__iregex=regex) |
            Q(author__iregex=regex) 
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
        regex = self.pattern_to_regex(pattern)
        return self.filter(Q(title__iregex=regex) 
          | Q(collection__title__iregex=regex))

    def by_publish_year(self, from_year, to_year = None):
        "Find items by publishing year"
        if to_year is None:
            to_year = from_year
        return self.filter(collection__year_published__range=(from_year, to_year)) 

    def by_change_time(self, from_time = None, until_time = None):
        "Find items by last change time"  
        return self._by_change_time('item', from_time, until_time)
            
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


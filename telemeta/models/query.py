# Copyright (C) 2007 Samalyse SARL
# All rights reserved.
#
# This software is licensed as described in the file COPYING, which
# you should have received as part of this distribution. The terms
# are also available at http://svn.parisson.org/telemeta/TelemetaLicense.
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
        regex = pattern;
        regex = regex.replace('*', '.*')
        regex = regex.replace('.', '.*')
        regex = regex.replace('-', '.*')
        regex = regex.replace(' ', '.*')
        return regex

    def word_search(self, field, pattern):
        regex = self.pattern_to_regex(pattern)
        kwargs = {field + '__iregex': regex}
        return self.filter(**kwargs)

class CoreManager(Manager):
    "Base class for all models managers"

    def none(self, *args, **kwargs):
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
        return self.filter(items__etat=country).distinct()
    
    def by_continent(self, continent):
        "Find collections by continent"
        return self.filter(items__continent=continent).distinct()

    def by_recording_date(self, pattern):
        return self.filter(annee_enr__icontains=pattern)

    def by_publish_date(self, pattern):
        return self.filter(date_published__icontains=pattern) 

    def by_ethnic_group(self, group):
        return self.filter(items__ethnie_grsocial=group).distinct()

class MediaCollectionManager(CoreManager):
    "Manage collection queries"

    def get_query_set(self):
        return MediaCollectionQuerySet(self.model)

    def quick_search(self, *args, **kwargs):
        return self.get_query_set().quick_search(*args, **kwargs)

    def by_country(self, *args, **kwargs):
        return self.get_query_set().by_country(*args, **kwargs)

    def by_continent(self, *args, **kwargs):
        return self.get_query_set().by_continent(*args, **kwargs)

    def by_recording_date(self, *args, **kwargs):
        return self.get_query_set().by_recording_date(*args, **kwargs)

    def by_publish_date(self, *args, **kwargs):
        return self.get_query_set().by_publish_date(*args, **kwargs)

    def by_ethnic_group(self, *args, **kwargs):
        return self.get_query_set().by_ethnic_group(*args, **kwargs)

    def stat_continents(self, order_by='num'):      
        "Return the number of collections by continents and countries as a tree"
        from django.db import connection
        cursor = connection.cursor()
        if order_by == 'num':
            order_by = 'items_num DESC'
        else:
            order_by = 'etat'
        cursor.execute("SELECT continent, etat, count(*) AS items_num "
            "FROM telemeta_collection INNER JOIN telemeta_item "
            "ON telemeta_collection.id = telemeta_item.collection_id "
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

        cursor.execute("SELECT DISTINCT(continent) FROM telemeta_item ORDER BY continent")
        result_set = cursor.fetchall()
        result = []
        for a, in result_set:
            if a != '' and a != 'N': # CREM fix
                result.append(a)
        
        return result

class MediaItemQuerySet(CoreQuerySet):
    
    def quick_search(self, pattern):
        "Perform a quick search on id and title"
        regex = self.pattern_to_regex(pattern)
        return self.filter(
            Q(id__iregex=regex) |
            Q(_title__iregex=regex) |
            Q(auteur__iregex=regex) 
        )

    def without_collection(self):        
        "Find items which do not belong to any collection"
        return self.extra(
            where = ["collection_id NOT IN (SELECT id FROM telemeta_collection)"]);

    def by_recording_date(self, pattern):
        "Find items by recording date"
        return self.filter(Q(dates_enregistr__icontains=pattern) 
            | Q(annee_enreg__icontains=pattern))

    def by_title(self, pattern):
        # to (sort of) sync with models.media.MediaItem.get_title()
        regex = self.pattern_to_regex(pattern)
        return self.filter(Q(_title__iregex=regex) 
          | Q(collection__title__iregex=regex))

    def by_publish_date(self, pattern):
        return self.filter(collection__date_published__icontains=pattern) 
            
class MediaItemManager(CoreManager):
    "Manage media items queries"

    def get_query_set(self):
        return MediaItemQuerySet(self.model)

    def quick_search(self, *args, **kwargs):
        return self.get_query_set().quick_search(*args, **kwargs)

    def without_collection(self, *args, **kwargs):
        return self.get_query_set().without_collection(*args, **kwargs)

    def by_recording_date(self, *args, **kwargs):
        return self.get_query_set().by_recording_date(*args, **kwargs)

    def by_title(self, *args, **kwargs):
        return self.get_query_set().by_title(*args, **kwargs)

    def by_publish_date(self, *args, **kwargs):
        return self.get_query_set().by_publish_date(*args, **kwargs)

    def list_ethnic_groups(self):
        "Return a list of all ethnic groups"
        
        from django.db import connection
        cursor = connection.cursor()

        cursor.execute("SELECT DISTINCT(ethnie_grsocial) FROM telemeta_item "
            "ORDER BY REPLACE(ethnie_grsocial, '\\'', '')")
        result_set = cursor.fetchall()
        result = []
        for a, in result_set:
            if a != '/' and a != '': # CREM fix
                result.append(a)
        
        return result


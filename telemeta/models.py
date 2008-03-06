# Copyright (C) 2007 Samalyse SARL
# All rights reserved.
#
# This software is licensed as described in the file COPYING, which
# you should have received as part of this distribution. The terms
# are also available at http://svn.parisson.org/telemeta/TelemetaLicense.
#
# Author: Olivier Guilyardi <olivier@samalyse.com>

from django.db.models import Manager, Model, Q, CharField, FileField, \
    TextField, DecimalField, ForeignKey, DateField
from django.db.models.query import QuerySet
from django.core.exceptions import ObjectDoesNotExist
from django.core import validators
from django.conf import settings

import telemeta
from telemeta.core import *
from telemeta import dublincore as dc
from xml.dom.minidom import getDOMImplementation

# Regular (sub) expression for matching/validating media objects IDs
media_id_regex = r'[0-9A-Za-z._-]+'

class MediaModel(Component):
    "Represent the whole model as a component"
    pass

class MediaCore(object):
    "Base class of all media objects"

    def to_dict(self):  
        "Return model fields as a dict of name/value pairs"
        fields_dict = {}
        for field in self._meta.fields:
            fields_dict[field.name] = getattr(self, field.name)
        return fields_dict

    def to_list(self):  
        "Return model fields as a list"
        fields_list = []
        for field in self._meta.fields:
            fields_list.append({'name': field.name, 'value': getattr(self, field.name)})
        return fields_list

    def get_dom_element_name(cls):
        "Convert the class name to a DOM element name"
        clsname = cls.__name__
        return clsname[0].lower() + clsname[1:]
    get_dom_element_name = classmethod(get_dom_element_name)

    def to_dom(self):
        "Return the DOM representation of this media object"
        impl = getDOMImplementation()
        root = self.get_dom_element_name()
        doc = impl.createDocument(None, root, None)
        top = doc.documentElement
        top.setAttribute("id", self.id)
        fields = self.to_dict()
        for name, value in fields.iteritems():
            element = doc.createElement(name)
            value = unicode(str(value), "utf-8")
            element.appendChild(doc.createTextNode(value))
            top.appendChild(element)
        return doc

class PhysicalFormat(Model):
    "Physical support of media items"

    value = CharField(maxlength=250)
    is_enumeration = True
    def __str__(self):
        return self.value
    class Meta:
        ordering = ['value']
        
class PublishingStatus(Model):
    "Publishing status of media items"
    value = CharField(maxlength=250)
    is_enumeration = True
    def __str__(self):
        return self.value
    class Meta:
        ordering = ['value']
        verbose_name_plural = "Publishing status"

class CoreQuerySet(QuerySet):
    "Base class for all query sets"

    def none(self): # redundant with none() in recent Django svn
        "Return an empty result set"
        return self.extra(where = ["0 = 1"])

class CoreManager(Manager):
    "Base class for all models managers"

    def none(self, *args, **kwargs):
        return self.get_query_set().none(*args, **kwargs)

class MediaCollectionQuerySet(CoreQuerySet):

    def quick_search(self, pattern):
        "Perform a quick search on id, title and creator name"
        return self.filter(
            Q(id__icontains=pattern) |
            Q(title__icontains=pattern) |
            Q(creator__icontains=pattern)
        )

    def by_country(self, country):
        "Find collections by country"
        return self.extra(where = ["id IN (SELECT collection_id "
            "FROM telemeta_item WHERE etat = %s)"],
            params=[country]);
    
    def by_continent(self, continent):
        "Find collections by continent"
        return self.extra(where = ["id IN (SELECT collection_id "
            "FROM telemeta_item WHERE continent = %s)"],
            params=[continent]);

    def by_recording_date(self, pattern):
        return self.filter(annee_enr__icontains=pattern)

    def by_publish_date(self, pattern):
        return self.filter(date_published__icontains=pattern) 

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

class MediaCollection(Model, MediaCore):
    "Group related media items"

    id_regex = media_id_regex
    id_validator = validators.MatchesRegularExpression('^' + id_regex + '$')

    publisher_reference = CharField(maxlength=250, blank=True)
    physical_format     = CharField(maxlength=250, blank=True)
    id                  = CharField(maxlength=250, primary_key=True, 
                        verbose_name='identifier', validator_list=[id_validator])
    title               = CharField(maxlength=250)
    native_title        = CharField(maxlength=250, blank=True)
    physical_items_num  = CharField(maxlength=250, blank=True) 
    publishing_status   = CharField(maxlength=250, blank=True)
    is_original         = CharField(maxlength=250, blank=True)
    is_full_copy        = CharField(maxlength=250, blank=True)
    copied_from         = ForeignKey('self', null=True, blank=True)
    creator             = CharField(maxlength=250)
    booklet_writer      = CharField(maxlength=250, blank=True)
    booklet_description = TextField(blank=True)
    collector           = CharField(maxlength=250, blank=True)
    publisher           = CharField(maxlength=250, blank=True)
    date_published      = CharField(maxlength=250, blank=True)
    publisher_collection= CharField(maxlength=250, blank=True)
    publisher_serial_id = CharField(maxlength=250, blank=True)
    ref_biblio          = TextField(blank=True)
    acquisition_mode    = CharField(maxlength=250, blank=True)
    comment             = TextField(blank=True)
    record_author       = CharField(maxlength=250, blank=True)
    record_writer       = CharField(maxlength=250, blank=True)
    rights              = CharField(maxlength=250, blank=True)
    annee_enr           = CharField(maxlength=250, blank=True)
    terrain_ou_autre    = CharField(maxlength=250, blank=True)
    duree_approx        = CharField(maxlength=250, blank=True)
    tri_dibm            = CharField(maxlength=250, blank=True)
    travail             = CharField(maxlength=250, blank=True)
    compil_face_plage   = TextField(blank=True)
    deposant_cnrs       = CharField(maxlength=250, blank=True)
    fiches              = CharField(maxlength=250, blank=True)
    a_informer          = CharField(maxlength=250, blank=True)
    numerisation        = CharField(maxlength=250, blank=True)
    champ36             = CharField(maxlength=250, blank=True)
     
    objects = MediaCollectionManager()

    def to_dublincore(self):
        "Express this collection as a Dublin Core resource"
        if (self.date_published):
            date = self.date_published
        else:
            date = self.annee_enr

        if (self.copied_from):
            copied_from = self.copied_from.id
        else:
            copied_from = ''

        resource = dc.Resource(
            dc.Element('identifier','id', self.id),
            dc.Element('type', value='Collection'),
            dc.Element('title', 'title', self.title),
            dc.Element('title', 'native_title', self.native_title),
            dc.Element('creator', 'creator', self.creator),
            dc.Element('relation', 'copied_from', copied_from, 'isVersionOf'),
            dc.Element('contributor', 'booklet_writer', self.booklet_writer),
            dc.Element('contributor', 'collector', self.collector),
            dc.Element('publisher', 'publisher', self.publisher),
            dc.Element('date', value=date),
            dc.Element('rights', 'rights', self.rights),
        )
        return resource

    def has_mediafile(self):
        "Tell wether this collection has any media files attached to its items"
        items = self.items.all()
        for item in items:
            if item.file:
                return True
        return False

    def __str__(self):
        #return self.title
        return self.id

    class Meta:
        ordering = ['title']
        db_table = 'telemeta_collection'

    class Admin:
        pass

class MediaItemQuerySet(CoreQuerySet):
    
    def quick_search(self, pattern):
        "Perform a quick search on id and title"
        return self.filter(
            Q(id__icontains=pattern) |
            Q(_title__icontains=pattern) 
        )

    def without_collection(self):        
        "Find items which do not belong to any collection"
        return self.extra(
            where = ["collection_id NOT IN (SELECT id FROM telemeta_collection)"]);

    def by_recording_date(self, pattern):
        return self.filter(Q(dates_enregistr__icontains=pattern) 
            | Q(annee_enreg__icontains=pattern))

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

class MediaItem(Model, MediaCore):
    "Describe an item with metadata" 

    id_regex = media_id_regex
    id_validator = validators.MatchesRegularExpression('^' + id_regex + '$')

    ref             = CharField(maxlength=250, blank=True)
    format          = CharField(maxlength=250, blank=True)
    collection      = ForeignKey(MediaCollection, related_name="items")
    face_plage      = CharField(maxlength=250, blank=True)
    id              = CharField(maxlength=250, primary_key=True, 
                    verbose_name='identifier', validator_list=[id_validator])
    duree           = CharField(maxlength=250, blank=True)
    dates_enregistr = CharField(maxlength=250, blank=True)
    etat            = CharField(maxlength=250, blank=True)
    region_village  = CharField(maxlength=250, blank=True)
    ethnie_grsocial = CharField(maxlength=250, blank=True)
    titre_support   = CharField(maxlength=250, blank=True)
    _title          = CharField(maxlength=250, db_column='title', blank=True)
    transcrip_trad  = CharField(maxlength=250, blank=True)
    auteur          = CharField(maxlength=250, blank=True)
    form_genr_style = CharField(maxlength=250, blank=True)
    struct_modale   = CharField(maxlength=250, blank=True)
    struct_rythm    = CharField(maxlength=250, blank=True)
    comm_fonctusage = TextField(blank=True)
    documentation   = TextField(maxlength=250, blank=True)
    remarques       = TextField(maxlength=250, blank=True)
    moda_execut     = CharField(maxlength=250, blank=True)
    copie_de        = CharField(maxlength=250, blank=True)
    enregistre_par  = CharField(maxlength=250, blank=True)
    aire_geo_cult   = CharField(maxlength=250, blank=True)
    annee_enreg     = CharField(maxlength=250, blank=True)
    formstyl_generi = CharField(maxlength=250, blank=True)
    choixcollecteur = CharField(maxlength=250, blank=True)
    repere_bande    = CharField(maxlength=250, blank=True)
    nroband_nropiec = CharField(maxlength=250, blank=True)
    continent       = CharField(maxlength=250, blank=True)
    file            = FileField(upload_to='items/%Y/%m/%d', blank=True)

    objects = MediaItemManager()

    def _get_title(self):
        if self._title == "":
            try:
                title = self.collection.title + " - Face/Plage: " \
                    + self.face_plage
            except ObjectDoesNotExist:
                title = self.id
        else:
            title = self._title

        return title
    title = property(_get_title)        

    def to_dublincore(self):
        "Express this item as a Dublin Core resource"
        if self.auteur:
            creator = self.auteur
        else: 
            creator = self.collection.creator

        resource = dc.Resource(
            dc.Element('identifier','id', self.id),
            dc.Element('type', value='Sound'),
            dc.Element('relation', 'collection', self.collection.id, 'isPartOf'),
            dc.Element('title', 'title', self.title),
            dc.Element('creator', value=creator),
            dc.Element('publisher', value=self.collection.publisher),
            dc.Element('coverage', value=self.etat),
        )
        return resource

    def get_duration(self):
        "Tell the length in seconds of this item media data"
        if self.file:
            import wave
            media = wave.open(settings.MEDIA_ROOT + "/" + self.file, "rb")
            duration = media.getnframes() / media.getframerate()
            media.close()
        else:
            duration = 0

        return duration

    def __str__(self):
        return self.title

    class Admin:
        pass

    class Meta:
        ordering = ['_title']
        db_table = 'telemeta_item'


class MediaPart(Model, MediaCore):
    "Describe the part of a media item"

    contributor = CharField(maxlength=250, blank=True)
    coverage    = CharField(maxlength=250, blank=True)
    creator     = CharField(maxlength=250, blank=True)
    date        = DateField()
    description = CharField(maxlength=250, blank=True)
    format      = CharField(maxlength=250, blank=True)
    identifier  = CharField(maxlength=250, blank=True)
    language    = CharField(maxlength=250, blank=True)
    publisher   = CharField(maxlength=250, blank=True)
    rights      = CharField(maxlength=250, blank=True)
    source      = CharField(maxlength=250, blank=True)
    subject     = CharField(maxlength=250, blank=True)
    title       = CharField(maxlength=250, blank=True)
    media_item  = ForeignKey(MediaItem)
    #media_item.dublin_core = 'relation'
    parent      = ForeignKey('self', null=True, related_name='children')
    #media_item.dublin_core = 'relation'
    start       = DecimalField(max_digits=11, decimal_places=3)
    end         = DecimalField(max_digits=11, decimal_places=3)
    #comment = TextField(blank=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']
        db_table = 'telemeta_part'

    class Admin:
        pass


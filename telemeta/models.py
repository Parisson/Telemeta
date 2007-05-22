# Copyright (C) 2007 Samalyse SARL
# All rights reserved.
#
# This software is licensed as described in the file COPYING, which
# you should have received as part of this distribution. The terms
# are also available at http://svn.parisson.org/telemeta/TelemetaLicense.
#
# Author: Olivier Guilyardi <olivier@samalyse.com>

from django.db import models
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from django.core import validators
from django.conf import settings

import telemeta
from telemeta.core import *
from telemeta import dublincore as dc
from xml.dom import getDOMImplementation

# Regular (sub) expression for matching/validating media objects IDs
media_id_regex = r'[0-9A-Za-z._:%?-]+'

class MediaModel(Component):
    pass

class MediaCore(object):
    def to_dict(self):  
        "Return model fields as a dict of name/value pairs"
        fields_dict = {}
        for field in self._meta.fields:
            fields_dict[field.name] = getattr(self, field.name)
        return fields_dict

    def get_dom_element_name(cls):
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

class PhysicalFormat(models.Model):
    value = models.CharField(maxlength=250)
    is_enumeration = True
    def __str__(self):
        return self.value
    class Meta:
        ordering = ['value']
        
class PublishingStatus(models.Model):
    value = models.CharField(maxlength=250)
    is_enumeration = True
    def __str__(self):
        return self.value
    class Meta:
        ordering = ['value']
        verbose_name_plural = "Publishing status"
        
class MediaCollectionManager(models.Manager):
    def quick_search(self, pattern):
        return super(MediaCollectionManager, self).get_query_set().filter(
            Q(id__icontains=pattern) |
            Q(title__icontains=pattern) |
            Q(creator__icontains=pattern)
        )

    def by_country(self, country):
        qs = super(MediaCollectionManager, self).get_query_set()
        return qs.extra(where = ["id IN (SELECT collection_id "
            "FROM telemeta_item WHERE etat = %s)"],
            params=[country]);

    def stat_continents(self):            
        from django.db import connection
        cursor = connection.cursor()
        cursor.execute("SELECT continent, etat, count(*) AS items_num "
            "FROM telemeta_collection INNER JOIN telemeta_item "
            "ON telemeta_collection.id = telemeta_item.collection_id "
            "WHERE (continent IN "
            "  ('EUROPE', 'OCEANIE', 'ASIE', 'AMERIQUE', 'AFRIQUE')) "
            "AND etat <> '' "
            "GROUP BY etat ORDER BY continent, items_num desc;")
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


class MediaCollection(models.Model, MediaCore):
    "Group related media items"

    id_regex = media_id_regex
    id_validator = validators.MatchesRegularExpression('^' + id_regex + '$')

    publisher_reference = models.CharField(maxlength=250, blank=True)
    physical_format = models.CharField(maxlength=250, blank=True)
    id = models.CharField(maxlength=250, primary_key=True, 
        verbose_name='identifier', validator_list=[id_validator])
    title = models.CharField(maxlength=250)
    native_title = models.CharField(maxlength=250, blank=True)
    physical_items_num = models.CharField(maxlength=250, blank=True) 
    publishing_status = models.CharField(maxlength=250, blank=True)
    is_original = models.CharField(maxlength=250, blank=True)
    is_full_copy = models.CharField(maxlength=250, blank=True)
    copied_from = models.ForeignKey('self', null=True, blank=True)
    creator = models.CharField(maxlength=250)
    booklet_writer = models.CharField(maxlength=250, blank=True)
    booklet_description = models.TextField(blank=True)
    collector = models.CharField(maxlength=250, blank=True)
    publisher = models.CharField(maxlength=250, blank=True)
    date_published = models.CharField(maxlength=250, blank=True)
    publisher_collection = models.CharField(maxlength=250, blank=True)
    publisher_serial_id = models.CharField(maxlength=250, blank=True)
    ref_biblio = models.TextField(blank=True)
    acquisition_mode = models.CharField(maxlength=250, blank=True)
    comment = models.TextField(blank=True)
    record_author = models.CharField(maxlength=250, blank=True)
    record_writer = models.CharField(maxlength=250, blank=True)
    rights = models.CharField(maxlength=250, blank=True)
    annee_enr = models.CharField(maxlength=250, blank=True)
    terrain_ou_autre = models.CharField(maxlength=250, blank=True)
    duree_approx = models.CharField(maxlength=250, blank=True)
    tri_dibm = models.CharField(maxlength=250, blank=True)
    travail = models.CharField(maxlength=250, blank=True)
    compil_face_plage = models.TextField(blank=True)
    deposant_cnrs = models.CharField(maxlength=250, blank=True)
    fiches = models.CharField(maxlength=250, blank=True)
    a_informer = models.CharField(maxlength=250, blank=True)
    numerisation = models.CharField(maxlength=250, blank=True)
    champ36 = models.CharField(maxlength=250, blank=True)
     
    objects = MediaCollectionManager()

    def to_dublincore(self):
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
            dc.Element('relation', 'copied_from', copied_from, 
                'isVersionOf'),
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

class MediaItemManager(models.Manager):
    def quick_search(self, pattern):
        return super(MediaItemManager, self).get_query_set().filter(
            Q(id__icontains=pattern) |
            Q(_title__icontains=pattern) 
        )

class MediaItem(models.Model, MediaCore):
    "Describe a item with metadata" 

    id_regex = media_id_regex
    id_validator = validators.MatchesRegularExpression('^' + id_regex + '$')

    ref = models.CharField(maxlength=250, blank=True)
    format = models.CharField(maxlength=250, blank=True)
    collection = models.ForeignKey(MediaCollection, related_name="items")
    face_plage = models.CharField(maxlength=250, blank=True)
    id = models.CharField(maxlength=250, primary_key=True, 
        verbose_name='identifier', validator_list=[id_validator])
    duree = models.CharField(maxlength=250, blank=True)
    dates_enregistr = models.CharField(maxlength=250, blank=True)
    etat = models.CharField(maxlength=250, blank=True)
    region_village = models.CharField(maxlength=250, blank=True)
    ethnie_grsocial = models.CharField(maxlength=250, blank=True)
    titre_support = models.CharField(maxlength=250, blank=True)
    _title = models.CharField(maxlength=250, db_column='title')
    transcrip_trad = models.CharField(maxlength=250, blank=True)
    auteur = models.CharField(maxlength=250, blank=True)
    form_genr_style = models.CharField(maxlength=250, blank=True)
    struct_modale = models.CharField(maxlength=250, blank=True)
    struct_rythm = models.CharField(maxlength=250, blank=True)
    comm_fonctusage = models.TextField(blank=True)
    documentation = models.TextField(maxlength=250, blank=True)
    remarques = models.TextField(maxlength=250, blank=True)
    moda_execut = models.CharField(maxlength=250, blank=True)
    copie_de = models.CharField(maxlength=250, blank=True)
    enregistre_par = models.CharField(maxlength=250, blank=True)
    aire_geo_cult = models.CharField(maxlength=250, blank=True)
    annee_enreg = models.CharField(maxlength=250, blank=True)
    formstyl_generi = models.CharField(maxlength=250, blank=True)
    choixcollecteur = models.CharField(maxlength=250, blank=True)
    repere_bande = models.CharField(maxlength=250, blank=True)
    nroband_nropiec = models.CharField(maxlength=250, blank=True)
    continent = models.CharField(maxlength=250, blank=True)
    file = models.FileField(upload_to='items/%Y/%m/%d', blank=True)

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


class MediaPart(models.Model, MediaCore):
    "Describe the part of a media item"

    contributor = models.CharField(maxlength=250)
    coverage = models.CharField(maxlength=250)
    creator = models.CharField(maxlength=250)
    date = models.DateField()
    description = models.CharField(maxlength=250)
    format = models.CharField(maxlength=250)
    identifier = models.CharField(maxlength=250)
    language = models.CharField(maxlength=250)
    publisher = models.CharField(maxlength=250)
    rights = models.CharField(maxlength=250)
    source = models.CharField(maxlength=250)
    subject = models.CharField(maxlength=250)
    title = models.CharField(maxlength=250)
    media_item = models.ForeignKey(MediaItem)
    media_item.dublin_core = 'relation'
    parent = models.ForeignKey('self', null=True, related_name='children')
    media_item.dublin_core = 'relation'
    start = models.DecimalField(max_digits=11, decimal_places=3)
    end = models.DecimalField(max_digits=11, decimal_places=3)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']
        db_table = 'telemeta_part'

    class Admin:
        pass


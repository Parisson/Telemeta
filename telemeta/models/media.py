# -*- coding: utf-8 -*-
# Copyright (C) 2007 Samalyse SARL
#
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

from django.db.models import Model, CharField, FileField, \
    TextField, DecimalField, ForeignKey, DateField, AutoField, \
    DateTimeField
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from xml.dom.minidom import getDOMImplementation
import re

import telemeta
from telemeta.core import *
from telemeta.models import dublincore as dc
from telemeta.models.query import MediaItemManager, MediaItemQuerySet, \
  MediaCollectionManager, MediaCollectionQuerySet

# Regular (sub) expression for matching/validating media objects IDs
# FIXME: need to use this in MediaCore.save()
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
            value = unicode(value)
            element.appendChild(doc.createTextNode(value))
            top.appendChild(element)
        return doc
    
    def is_well_formed_id(cls, value):
        regex = re.compile(r"^" + media_id_regex + r"$")
        if regex.match(value):
            return True 
        else:
            return False
    is_well_formed_id = classmethod(is_well_formed_id)


class MediaCollection(Model, MediaCore):
    "Group related media items"

    id_regex = media_id_regex

    publisher_reference = CharField(max_length=250, blank=True)
    physical_format     = CharField(max_length=250, blank=True)
    id                  = CharField(max_length=250, primary_key=True,
                          verbose_name='identifier')
    title               = CharField(max_length=250)
    native_title        = CharField(max_length=250, blank=True)
    physical_items_num  = CharField(max_length=250, blank=True) 
    publishing_status   = CharField(max_length=250, blank=True)
    is_original         = CharField(max_length=250, blank=True)
    is_full_copy        = CharField(max_length=250, blank=True)
    copied_from         = ForeignKey('self', null=True, blank=True)
    creator             = CharField(max_length=250)
    booklet_writer      = CharField(max_length=250, blank=True)
    booklet_description = TextField(blank=True)
    collector           = CharField(max_length=250, blank=True)
    publisher           = CharField(max_length=250, blank=True)
    date_published      = CharField(max_length=250, blank=True)
    publisher_collection= CharField(max_length=250, blank=True)
    publisher_serial_id = CharField(max_length=250, blank=True)
    ref_biblio          = TextField(blank=True)
    acquisition_mode    = CharField(max_length=250, blank=True)
    comment             = TextField(blank=True)
    record_author       = CharField(max_length=250, blank=True)
    record_writer       = CharField(max_length=250, blank=True)
    rights              = CharField(max_length=250, blank=True)
    annee_enr           = CharField(max_length=250, blank=True)
    terrain_ou_autre    = CharField(max_length=250, blank=True)
    duree_approx        = CharField(max_length=250, blank=True)
    tri_dibm            = CharField(max_length=250, blank=True)
    travail             = CharField(max_length=250, blank=True)
    compil_face_plage   = TextField(blank=True)
    deposant_cnrs       = CharField(max_length=250, blank=True)
    fiches              = CharField(max_length=250, blank=True)
    a_informer          = CharField(max_length=250, blank=True)
    numerisation        = CharField(max_length=250, blank=True)
    champ36             = CharField(max_length=250, blank=True)
     
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

    def is_published(self):
        if len(self.publisher_reference) < 3:
          return True
        if self.publisher_reference[:3] == 'BM.':
          return False
        return True

    def ordered_items(self):
        return self.items.order_by('id', '_title')

    def get_countries(self):
        countries = []
        items = self.items.order_by('etat')
        for item in items:
            if not item.etat in countries and item.etat:
                countries.append(item.etat)
        return countries

    def get_ethnic_groups(self):
        groups = []
        items = self.items.order_by('ethnie_grsocial')
        for item in items:
            if not item.ethnie_grsocial in groups and item.ethnie_grsocial:
                groups.append(item.ethnie_grsocial)
        return groups

    def __unicode__(self):
        #return self.title
        return self.id

    def save(self, force_insert=False, force_update=False):
        if not MediaCore.is_well_formed_id(self.id):
            raise MediaInvalidIdError()
        super(MediaCollection, self).save(force_insert, force_update)
        Revision(element_type='collection', element_id=self.id).touch()
        
    def get_revision(self):
        return Revision.objects.filter(element_type='collection', element_id=self.id).order_by('-time')[0]

    class Meta:
        app_label = 'telemeta'
        ordering = ['title']
        db_table = 'telemeta_collection'

class MediaItem(Model, MediaCore):
    "Describe an item with metadata" 

    id_regex = media_id_regex

    ref             = CharField(max_length=250, blank=True)
    format          = CharField(max_length=250, blank=True)
    collection      = ForeignKey(MediaCollection, related_name="items")
    face_plage      = CharField(max_length=250, blank=True)
    id              = CharField(max_length=250, primary_key=True, 
                      verbose_name='identifier')
    duree           = CharField(max_length=250, blank=True)
    dates_enregistr = CharField(max_length=250, blank=True)
    etat            = CharField(max_length=250, blank=True)
    region_village  = CharField(max_length=250, blank=True)
    ethnie_grsocial = CharField(max_length=250, blank=True)
    titre_support   = CharField(max_length=250, blank=True)
    _title          = CharField(max_length=250, db_column='title', blank=True)
    transcrip_trad  = CharField(max_length=250, blank=True)
    auteur          = CharField(max_length=250, blank=True)
    form_genr_style = CharField(max_length=250, blank=True)
    struct_modale   = CharField(max_length=250, blank=True)
    struct_rythm    = CharField(max_length=250, blank=True)
    comm_fonctusage = TextField(blank=True)
    documentation   = TextField(max_length=250, blank=True)
    remarques       = TextField(max_length=250, blank=True)
    moda_execut     = CharField(max_length=250, blank=True)
    copie_de        = CharField(max_length=250, blank=True)
    enregistre_par  = CharField(max_length=250, blank=True)
    aire_geo_cult   = CharField(max_length=250, blank=True)
    annee_enreg     = CharField(max_length=250, blank=True)
    formstyl_generi = CharField(max_length=250, blank=True)
    choixcollecteur = CharField(max_length=250, blank=True)
    repere_bande    = CharField(max_length=250, blank=True)
    nroband_nropiec = CharField(max_length=250, blank=True)
    continent       = CharField(max_length=250, blank=True)
    file            = FileField(upload_to='items/%Y/%m/%d', blank=True)

    objects = MediaItemManager()

    def _get_title(self):
        # to (sort of) sync with models.query.MediaItemQuerySet.by_title()
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

        duration = self.get_duration()
        duration = "%02d:%02d:%02d" % (duration / 3600, duration % 3600 / 60, duration % 3600 % 60)

        resource = dc.Resource(
            dc.Element('identifier','id', self.id),
            dc.Element('type', value='Sound'),
            dc.Element('relation', 'collection', self.collection.id, 'isPartOf'),
            dc.Element('title', 'title', self.title),
            dc.Element('creator', value=creator),
            dc.Element('description', value=self.comm_fonctusage),
            dc.Element('publisher', value=self.collection.publisher),
            dc.Element('coverage', value=self.etat),
            dc.Element('format', value=duration, refinement="extent"),
            dc.Element('rights', value=self.collection.rights)
        )
        return resource

    def get_duration(self):
        "Tell the length in seconds of this item media data"
        if self.file:
            import wave
            media = wave.open(self.file.path, "rb")
            duration = media.getnframes() / media.getframerate()
            media.close()
        else:
            duration = 0

        return duration

    def get_revision(self):
        return Revision.objects.filter(element_type='item', element_id=self.id).order_by('-time')[0]

    def __unicode__(self):
        return self.title

    def save(self, force_insert=False, force_update=False):
        if not MediaCore.is_well_formed_id(self.id):
            raise MediaInvalidIdError()
        super(MediaItem, self).save(force_insert, force_update)
        Revision(element_type='item', element_id=self.id).touch()
        
    class Meta:
        app_label = 'telemeta'
        ordering = ['_title']
        db_table = 'telemeta_item'


class MediaPart(Model, MediaCore):
    "Describe the part of a media item"

    contributor = CharField(max_length=250, blank=True)
    coverage    = CharField(max_length=250, blank=True)
    creator     = CharField(max_length=250, blank=True)
    date        = DateField()
    description = CharField(max_length=250, blank=True)
    format      = CharField(max_length=250, blank=True)
    identifier  = CharField(max_length=250, blank=True)
    language    = CharField(max_length=250, blank=True)
    publisher   = CharField(max_length=250, blank=True)
    rights      = CharField(max_length=250, blank=True)
    source      = CharField(max_length=250, blank=True)
    subject     = CharField(max_length=250, blank=True)
    title       = CharField(max_length=250, blank=True)
    media_item  = ForeignKey(MediaItem)
    #media_item.dublin_core = 'relation'
    parent      = ForeignKey('self', null=True, related_name='children')
    #media_item.dublin_core = 'relation'
    start       = DecimalField(max_digits=11, decimal_places=3)
    end         = DecimalField(max_digits=11, decimal_places=3)
    #comment = TextField(blank=True)

    def __unicode__(self):
        return self.title

    def save(self, force_insert=False, force_update=False):
        super(MediaPart, self).save(force_insert, force_update)
        Revision(element_type='part', element_id=self.id).touch()

    def get_revision(self):
        return Revision.objects.filter(element_type='part', element_id=self.id).order_by('-time')[0]

    class Meta:
        app_label = 'telemeta'
        ordering = ['title']
        db_table = 'telemeta_part'

class Revision(Model):
    id              = AutoField(primary_key=True)
    element_type    = CharField(max_length=16, choices=(('collection', 'collection'),
                                                        ('item', 'item'),
                                                        ('part', 'part')))
    element_id      = CharField(max_length=250, db_index=True)
    change_type     = CharField(max_length=8, choices= (('import', 'import'),
                                                        ('create', 'create'),
                                                        ('update', 'update'),
                                                        ('delete', 'delete')))
    time            = DateTimeField(auto_now_add=True)


    def touch(self):
        q = Revision.objects.filter(element_type=self.element_type, element_id=self.element_id) 
        if q.count():
            self.change_type = 'update'
        else:
            self.change_type = 'create'
        self.save()

    class Meta:
        app_label = 'telemeta'
        db_table = 'telemeta_revision'

class MediaInvalidIdError(Exception):
    pass

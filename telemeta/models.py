# Copyright (C) 2007 Samalyse SARL
# All rights reserved.
#
# This software is licensed as described in the file COPYING, which
# you should have received as part of this distribution. The terms
# are also available at http://svn.parisson.org/telemeta/TelemetaLicense.
#
# Author: Olivier Guilyardi <olivier@samalyse.com>

import telemeta
from django.db import models
from django.db.models import Q
from telemeta.core import *
from django.core.exceptions import ObjectDoesNotExist

class MediaModel(Component):
    pass

class MediaCore:
    def list(self):
        fields_list = []
        for field in self._meta.fields:
            fields_list.append({'name': field.verbose_name, 'value': getattr(self, field.name)})
        return fields_list

    def to_dict(self):        
        fields_dict = {}
        for field in self._meta.fields:
            fields_dict[field.name] = getattr(self, field.name)
        return fields_dict

class PhysicalFormat(models.Model):
    value = models.CharField(maxlength=250)
    is_dictionary = True
    def __str__(self):
        return self.value
    class Meta:
        ordering = ['value']
        
class MediaCollectionManager(models.Manager):
    def quick_search(self, pattern):
        return super(MediaCollectionManager, self).get_query_set().filter(
            Q(id__icontains=pattern) |
            Q(title__icontains=pattern) |
            Q(creator__icontains=pattern)
        )


class MediaCollection(models.Model, MediaCore):
    "Group related media items"

    publisher_reference = models.CharField(maxlength=250, blank=True)
    physical_format = models.CharField(maxlength=250, blank=True)
    id = models.CharField(maxlength=250, primary_key=True, 
        verbose_name='identifier')
    id.dc_element = 'identifier'
    title = models.CharField(maxlength=250)
    title.dc_element = 'title'
    native_title = models.CharField(maxlength=250, blank=True)
    native_title.dc_element = 'title'
    physical_items_num = models.CharField(maxlength=250, blank=True) 
    publishing_status = models.CharField(maxlength=250, blank=True)
    is_original = models.CharField(maxlength=250)
    is_full_copy = models.CharField(maxlength=250)
    copied_from = models.ForeignKey('self', blank=True)
    #copied_from[0].dc_element = 'relation'
    creator = models.CharField(maxlength=250)
    creator.dc_element = 'creator'
    booklet_writer = models.CharField(maxlength=250, blank=True)
    booklet_writer.dc_element = 'contributor'
    booklet_description = models.TextField(blank=True)
    collector = models.CharField(maxlength=250, blank=True)
    collector.dc_element = 'contributor'
    publisher = models.CharField(maxlength=250, blank=True)
    publisher.dc_element = 'publisher'
    date_published = models.CharField(maxlength=250, blank=True)
    date_published.dc_element = 'date'
    publisher_collection = models.CharField(maxlength=250, blank=True)
    publisher_serial_id = models.CharField(maxlength=250, blank=True)
    ref_biblio = models.TextField(blank=True)
    acquisition_mode = models.CharField(maxlength=250, blank=True)
    comment = models.TextField(blank=True)
    record_author = models.CharField(maxlength=250, blank=True)
    record_writer = models.CharField(maxlength=250, blank=True)
    rights = models.CharField(maxlength=250, blank=True)
    rights.dc_element = 'rights'
    annee_enr = models.CharField(maxlength=250, blank=True)
    annee_enr.dc_element = 'date'
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
     
#    date = models.DateField()
#    contributor = models.CharField(maxlength=250, blank=True)
#    coverage = models.CharField(maxlength=250, blank=True)
#    creator = models.CharField(maxlength=250, blank=True)
#    description = models.CharField(maxlength=250, blank=True)
#    format = models.CharField(maxlength=250, blank=True)
#    identifier = models.CharField(maxlength=250, blank=True)
#    language = models.CharField(maxlength=250, blank=True)
#    publisher = models.CharField(maxlength=250, blank=True)
#    rights = models.CharField(maxlength=250, blank=True)
#    source = models.CharField(maxlength=250, blank=True)
#    subject = models.CharField(maxlength=250, blank=True)
#    physical_format = models.ForeignKey(PhysicalFormat, null=True, blank=True)

    objects = MediaCollectionManager()

    def __str__(self):
        return self.title

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

    ref = models.CharField(maxlength=250, blank=True)
    format = models.CharField(maxlength=250, blank=True)
    collection = models.ForeignKey(MediaCollection, related_name="items")
    face_plage = models.CharField(maxlength=250, blank=True)
    id = models.CharField(maxlength=250, primary_key=True, 
        verbose_name='identifier')
    duree = models.CharField(maxlength=250, blank=True)
    dates_enregistr = models.CharField(maxlength=250, blank=True)
    etat = models.CharField(maxlength=250, blank=True)
    region_village = models.CharField(maxlength=250, blank=True)
    ethnie_grsocial = models.CharField(maxlength=250, blank=True)
    titre_support = models.CharField(maxlength=250, blank=True)
    _title = models.CharField(maxlength=250, db_column='title', blank=True)
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
    file = models.FileField(upload_to='items/%Y/%m/%d')

#    collection.dublin_core = 'relation'
#    identifier = models.CharField(maxlength=250)
#    title = models.CharField(maxlength=250)
#    creator = models.CharField(maxlength=250)
#    date = models.DateField()
#    file = models.FileField(upload_to='items/%Y/%m/%d')
#    subject = models.CharField(maxlength=250, blank=True)
#    description = models.TextField(maxlength=250, blank=True)
#    contributor = models.CharField(maxlength=250, blank=True)
#    coverage = models.CharField(maxlength=250, blank=True)
#    format = models.CharField(maxlength=25, blank=True)
#    language = models.CharField(maxlength=250, blank=True)
#    publisher = models.CharField(maxlength=250, blank=True)
#    rights = models.CharField(maxlength=250, blank=True)
#    source = models.CharField(maxlength=250, blank=True)
#    duration = models.FloatField(max_digits=11, decimal_places=3, null=True, blank=True)
#
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
    start = models.FloatField(max_digits=11, decimal_places=3)
    end = models.FloatField(max_digits=11, decimal_places=3)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']
        db_table = 'telemeta_part'

    class Admin:
        pass


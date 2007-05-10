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

class MediaModel(Component):
    pass

class MediaCore:
    def list(self):
        fields_list = []
        for field in self._meta.fields:
            fields_list.append({'name': field.name, 'value': getattr(self, field.name)})
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
            Q(title__icontains=pattern) |
            Q(creator__icontains=pattern)
        )


class MediaCollection(models.Model, MediaCore):
    "Group related media items"

    publisher_reference = models.CharField(maxlength=250, blank=True)
    physical_format = models.CharField(maxlength=250, blank=True)
    id = models.CharField(maxlength=250, primary_key=True)
    id.dc_element = 'identifier'
    title = models.CharField(maxlength=250)
    title.dc_element = 'title'
    native_title = models.CharField(maxlength=250, blank=True)
    native_title.dc_element = 'title'
    physical_items_num = models.IntegerField(blank=True) 
    publishing_status = models.CharField(maxlength=250, blank=True)
    is_original = models.CharField(maxlength=250)
    is_full_copy = models.CharField(maxlength=250)
    copied_from = models.ForeignKey('self', null=True),
    copied_from[0].dc_element = 'relation'
    creator = models.CharField(maxlength=250)
    creator.dc_element = 'creator'
    booklet_writer = models.CharField(maxlength=250, blank=True)
    booklet_writer.dc_element = 'contributor'
    booklet_description = models.TextField(blank=True)
    collector = models.CharField(maxlength=250, blank=True)
    collector.dc_element = 'contributor'
    publisher = models.CharField(maxlength=250, blank=True)
    publisher.dc_element = 'publisher'
    date_published = models.IntegerField(blank=True)
    date_published.dc_element = 'date'
    publisher_collection = models.CharField(maxlength=250, blank=True)
    publisher_serial_id = models.IntegerField(blank=True)
    ref_biblio = models.CharField(maxlength=250, blank=True)
    acquisition_mode = models.CharField(maxlength=250, blank=True)
    comment = models.TextField(blank=True)
    record_author = models.CharField(maxlength=250, blank=True)
    record_writer = models.CharField(maxlength=250, blank=True)
    rights = models.CharField(maxlength=250, blank=True)
    rights.dc_element = 'rights'
    annee_enr = models.IntegerField(blank=True)
    annee_enr.dc_element = 'date'
    terrain_ou_autre = models.CharField(maxlength=250, blank=True)
    duree_approx = models.CharField(maxlength=250, blank=True)
    tri_dibm = models.IntegerField(blank=True)
    travail = models.CharField(maxlength=250, blank=True)
    compil_face_plage = models.CharField(maxlength=250, blank=True)
    deposant_cnrs = models.CharField(maxlength=250, blank=True)
    fiches = models.CharField(maxlength=250, blank=True)
    a_informer = models.IntegerField(blank=True)
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
            Q(title__icontains=pattern) |
            Q(creator__icontains=pattern) |
            Q(identifier__icontains=pattern) |
            Q(description__icontains=pattern) 
        )

class MediaItem(models.Model, MediaCore):
    "Describe a item with metadata" 

    collection = models.ForeignKey(MediaCollection, related_name="items")
    collection.dublin_core = 'relation'
    identifier = models.CharField(maxlength=250)
    title = models.CharField(maxlength=250)
    creator = models.CharField(maxlength=250)
    date = models.DateField()
    file = models.FileField(upload_to='items/%Y/%m/%d')
    subject = models.CharField(maxlength=250, blank=True)
    description = models.TextField(maxlength=250, blank=True)
    contributor = models.CharField(maxlength=250, blank=True)
    coverage = models.CharField(maxlength=250, blank=True)
    format = models.CharField(maxlength=25, blank=True)
    language = models.CharField(maxlength=250, blank=True)
    publisher = models.CharField(maxlength=250, blank=True)
    rights = models.CharField(maxlength=250, blank=True)
    source = models.CharField(maxlength=250, blank=True)
    duration = models.FloatField(max_digits=11, decimal_places=3, null=True, blank=True)

    objects = MediaItemManager()

    def __str__(self):
        return self.title

    class Admin:
        pass

    class Meta:
        ordering = ['title']
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


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

class MediaCollectionManager(models.Manager):
    def quick_search(self, pattern):
        return super(MediaCollectionManager, self).get_query_set().filter(
            Q(title__icontains=pattern) |
            Q(description__icontains=pattern)
        )

class MediaCollection(models.Model, MediaCore):
    "Group related media items"

    title = models.CharField(maxlength=250)
    date = models.DateField()
    contributor = models.CharField(maxlength=250, blank=True)
    coverage = models.CharField(maxlength=250, blank=True)
    creator = models.CharField(maxlength=250, blank=True)
    description = models.CharField(maxlength=250, blank=True)
    format = models.CharField(maxlength=250, blank=True)
    identifier = models.CharField(maxlength=250, blank=True)
    language = models.CharField(maxlength=250, blank=True)
    publisher = models.CharField(maxlength=250, blank=True)
    rights = models.CharField(maxlength=250, blank=True)
    source = models.CharField(maxlength=250, blank=True)
    subject = models.CharField(maxlength=250, blank=True)

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



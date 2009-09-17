from django.db import models

class MediaCollection(models.Model):
    PUBLIC_ACCESS_CHOICES = (('0', 'none'), ('1', 'metadata'), ('2', 'full'))

    reference             = models.CharField(unique=True, max_length=250)
    physical_format       = models.ForeignKey('PhysicalFormat')
    old_code              = models.CharField(unique=True, max_length=250)
    code                  = models.CharField(unique=True, max_length=250)
    title                 = models.CharField(max_length=250)
    alt_title             = models.CharField(max_length=250)
    physical_items_num    = models.IntegerField()
    publishing_status     = models.ForeignKey('PublishingStatus')
    creator               = models.CharField(max_length=250)
    booklet_author        = models.CharField(max_length=250)
    booklet_description   = models.TextField()
    collector             = models.CharField(max_length=250)
    collector_is_creator  = models.BooleanField()
    publisher_id          = models.IntegerField()
    year_published        = models.IntegerField()
    publisher_collection  = models.ForeignKey('PublisherCollection')
    publisher_serial      = models.CharField(max_length=250)
    external_references   = models.TextField()
    acquisition_mode      = models.ForeignKey('AcquisitionMode')
    comment               = models.TextField()
    metadata_author       = models.ForeignKey('MetadataAuthor')
    metadata_writer       = models.ForeignKey('MetadataWriter')
    legal_rights          = models.ForeignKey('LegalRight')
    alt_ids               = models.CharField(max_length=250)
    recorded_from_year    = models.IntegerField()
    recorded_to_year      = models.IntegerField()
    recording_context     = models.ForeignKey('RecordingContext')
    approx_duration       = models.TimeField()
    doctype_code          = models.IntegerField()
    travail               = models.CharField(max_length=250)
    state                 = models.TextField()
    cnrs_contributor      = models.CharField(max_length=250)
    items_done            = models.CharField(max_length=250)
    a_informer_07_03      = models.CharField(max_length=250)
    ad_conversion         = models.ForeignKey('AdConversion')
    public_access         = models.CharField(choices=PUBLIC_ACCESS_CHOICES, max_length=250)

class MediaItem(models.Model):
    PUBLIC_ACCESS_CHOICES = (('0', 'none'), ('1', 'metadata'), ('2', 'full'))

    collection            = models.ForeignKey('MediaCollection', related_name="items")
    track                 = models.CharField(max_length=250)
    old_code              = models.CharField(unique=True, max_length=250)
    code                  = models.CharField(unique=True, max_length=250)
    approx_duration       = models.TimeField()
    recorded_from_date    = models.DateField()
    recorded_to_date      = models.DateField()
    location_name         = models.ForeignKey('Location')
    location_comment      = models.CharField(max_length=250)
    ethnic_group          = models.ForeignKey('EthnicGroup')
    title                 = models.CharField(max_length=250)
    alt_title             = models.CharField(max_length=250)
    author                = models.CharField(max_length=250)
    vernacular_style      = models.ForeignKey('VernacularStyle')
    context_comment       = models.TextField()
    external_references   = models.TextField()
    moda_execut           = models.CharField(max_length=250)
    copied_from_item      = models.ForeignKey('self')
    collector             = models.CharField(max_length=250)
    cultural_area         = models.CharField(max_length=250)
    generic_style         = models.ForeignKey('GenericStyle')
    collector_selection   = models.CharField(max_length=250)
    creator_reference     = models.CharField(max_length=250)
    comment               = models.TextField()
    filename              = models.CharField(max_length=250)
    public_access         = models.CharField(choices=PUBLIC_ACCESS_CHOICES, max_length=250)

class MediaPart(models.Model):
    item  = models.ForeignKey('MediaItem', related_name="parts")
    title = models.CharField(max_length=250)
    start = models.FloatField()
    end   = models.FloatField()

class PhysicalFormat(models.Model):
    value = models.CharField(max_length=250)

class PublishingStatus(models.Model):
    value = models.CharField(max_length=250)

class PublisherCollection(models.Model):
    value = models.CharField(max_length=250)

class AcquisitionMode(models.Model):
    value = models.CharField(max_length=250)

class MetadataAuthor(models.Model):
    value = models.CharField(max_length=250)

class MetadataWriter(models.Model):  
    value = models.CharField(max_length=250)

class LegalRight(models.Model): 
    value = models.CharField(max_length=250)

class RecordingContext(models.Model):
    value = models.CharField(max_length=250)

class AdConversion(models.Model):
    value = models.CharField(max_length=250)

class EthnicGroup(models.Model):
    value = models.CharField(max_length=250)
   
class VernacularStyle(models.Model):
    value = models.CharField(max_length=250)

class GenericStyle(models.Model):
    value = models.CharField(max_length=250)

class Instrument(models.Model):
    name    = models.CharField(max_length=250)
    parents = models.ManyToManyField("self")
    alias   = models.ManyToManyField("InstrumentAlias")

class InstrumentAlias(models.Model):
    name = models.CharField(max_length=250)

class MediaItemPerformance(models.Model):
    media_item      = models.ForeignKey('MediaItem')
    instrument      = models.ForeignKey('Instrument')
    alias           = models.ForeignKey('InstrumentAlias')
    instruments_num = models.CharField(max_length=250)
    musicians       = models.CharField(max_length=250)

class User(models.Model):
    LEVEL_CHOICES = (('0', 'user'), ('1', 'maintainer'), ('2', 'admin'))    

    username   = models.CharField(primary_key=True, max_length=250)
    level      = models.CharField(choices=LEVEL_CHOICES, max_length=250)
    first_name = models.CharField(max_length=250)
    last_name  = models.CharField(max_length=250)
    phone      = models.CharField(max_length=250)
    email      = models.CharField(max_length=250)

class Playlist(models.Model):
    owner_username = models.ForeignKey('self') 
    name           = models.CharField(max_length=250)

class PlaylistResource(models.Model):
    RESOURCE_TYPE_CHOICES = (('0', 'item'), ('1', 'collection'))

    playlist              = models.ForeignKey('Playlist')
    resource_type         = models.CharField(choices=RESOURCE_TYPE_CHOICES, max_length=250)
    resource              = models.IntegerField()

class Location(models.Model):
    TYPE_CHOICES     = (('0', 'country'), ('1', 'continent'), ('2', 'other'))

    name             = models.CharField(primary_key=True, max_length=250)
    type             = models.CharField(choices=TYPE_CHOICES, max_length=250)
    complet_type     = models.ForeignKey('LocationType')
    current_name     = models.ForeignKey('self') 
    is_authoritative = models.BooleanField()

class LocationType(models.Model):
    type = models.CharField(max_length=250)

class LocationAlias(models.Model):
    location_name    = models.ForeignKey('Location')
    alias            = models.CharField(max_length=250)
    is_authoritative = models.BooleanField()
    
class LocationRelation(models.Model):
    location_name        = models.ForeignKey('Location')
    parent_location_name = models.ForeignKey('Location')
    is_authoritative     = models.BooleanField()
    
class ContextKeyword(models.Model):
    value = models.CharField(max_length=250)

class MediaItemKeyword(models.Model):
    item    = models.ForeignKey('MediaItem')
    keyword = models.ForeignKey('ContextKeyword')

class Publisher(models.Model): 
    value = models.CharField(max_length=250)

class PublisherCollection(models.Model):
    publisher = models.ForeignKey('Publisher')
    value     = models.CharField(max_length=250)

class Revision(models.Model):
    CHANGE_TYPE_CHOICES = (('0', 'create'), ('1', 'update'), ('2','delete'))

    element_type        = models.CharField(max_length=250)
    element             = models.ForeignKey('User')
    change_type         = models.CharField(choices=CHANGE_TYPE_CHOICES, max_length=250)
    time                = models.DateTimeField()
    username            = models.ForeignKey('User')
    
class EthnicGroup(models.Model):
    name = models.CharField(max_length=250)

class EthnicGroupAlias(models.Model):
    ethnic_group = models.ForeignKey('EthnicGroup')
    name         = models.CharField(max_length=250)

from django.db import models

class MediaCollection(models.Model):
    PUBLIC_ACCESS_CHOICES = (('none'), ('metadata'), ('full'))

    reference             = models.CharField(unique=True)
    physical_format       = models.ForeignKey('PhysicalFormat')
    old_code              = models.CharField(unique=True)
    code                  = models.CharField(unique=True)
    title                 = models.CharField()
    alt_title             = models.CharField()
    physical_items_num    = models.IntegerField()
    publishing_status     = models.ForeignKey('PublishingStatus')
    creator               = models.CharField()
    booklet_author        = models.CharField()
    booklet_description   = models.TextField()
    collector             = models.CharField()
    collector_is_creator  = models.BooleanField()
    publisher_id          = models.IntegerField()
    year_published        = models.IntegerField()
    publisher_collection  = models.ForeignKey('PublisherCollection')
    publisher_serial      = models.CharField()
    external_references   = models.TextField()
    acquisition_mode      = models.ForeignKey('AcquisitionMode')
    comment               = models.TextField()
    metadata_author       = models.ForeignKey('MetadataAuthor')
    metadata_writer       = models.ForeignKey('MetadataWriter')
    legal_rights          = models.ForeignKey('LegalRight')
    alt_ids               = models.CharField()
    recorded_from_year    = models.IntegerField()
    recorded_to_year      = models.IntegerField()
    recording_context     = models.ForeignKey('RecordingContext')
    approx_duration       = models.TimeField()
    doctype_code          = models.IntegerField()
    travail               = models.CharField()
    state                 = models.TextField()
    cnrs_contributor      = models.CharField()
    items_done            = models.CharField()
    a_informer_07_03      = models.CharField()
    ad_conversion         = models.ForeignKey('AdConversion')
    public_access         = models.Charfield(choices=PUBLIC_ACCESS_CHOICES)

class MediaItem(models.Model):
    PUBLIC_ACCESS_CHOICES = (('none'), ('metadata'), ('full'))

    collection            = models.ForeignKey('MediaCollection')
    track                 = models.CharField()
    old_code              = models.CharField(unique=True)
    code                  = models.CharField(unique=True)
    approx_duration       = models.TimeField()
    recorded_from_date    = models.DateField()
    recorded_to_date      = models.DateField()
    location_name         = models.ForeignKey('Location')
    location_comment      = models.CharField()
    ethnic_group          = models.ForeignKey('EthnicGroup')
    title                 = models.CharField()
    alt_title             = models.CharField()
    author                = models.CharField()
    vernacular_style      = models.ForeignKey('VernacularStyle')
    context_comment       = models.TextField()
    external_references   = models.TextField()
    moda_execut           = models.CharField()
    copied_from_item      = models.ForeignKey('self')
    collector             = models.CharField()
    cultural_area         = models.CharField()
    generic_style         = models.ForeignKey('GenericStyle')
    collector_selection   = models.CharField()
    creator_reference     = models.CharField()
    comment               = models.TextField()
    filename              = models.CharField()
    public_access         = models.Charfield(choices=PUBLIC_ACCESS_CHOICES)

class MediaPart(models.Model):
    item  = models.ForeignKey('MediaItem')
    title = models.CharField()
    start = models.FloatField()
    end   = models.FloatField()

class PhysicalFormat(models.Model):
    value = models.CharField()

class PublishingStatus(models.Model):
    value = models.CharField()

class PublisherCollection(models.Model):
    value = models.CharField()

class AcquisitionMode(models.Model):
    value = models.CharField()

class MetadataAuthor(models.Model):
    value = models.CharField()

class MetadataWriter(models.Model):  
    value = models.CharField()

class LegalRight(models.Model): 
    value = models.CharField()

class RecordingContext(models.Model):
    value = models.CharField()

class AdConversion(models.Model):
    value = models.CharField()

class EthnicGroup(models.Model):
    value = models.CharField()
   
class VernacularStyle(models.Model):
    value = models.CharField()

class GenericStyle(models.Model):
    value = models.CharField()

class Instrument(models.Model):
    name = models.CharField()

class InstrumentRelation(models.Model):
    instrument        = models.ForeignKey('Instrument')
    parent_instrmuent = models.ForeignKey('Instrument')

class InstrumentAlias(models.Model):
    name = models.CharField()

class InstrumentAliasRelation(models.Model):
    alias      = models.ForeignKey('InstrumentAlias')
    instrument = models.ForeignKey('InstrumentAlias')

class MediaItemPerformance(models.Model):
    media_item      = models.ForeignKey('MediaItem')
    instrument      = models.ForeignKey('Instrument')
    alias           = models.ForeignKey('InstrumentAlias')
    instruments_num = models.CharField()
    musicians       = models.CharField()

class User(models.Model):
    LEVEL_CHOICES = (('user'), ('maintainer'), ('admin'))    

    username   = models.CharField(primary_key=True)
    level      = models.CharField(choices=LEVEL_CHOICES)
    first_name = models.CharField()
    last_name  = models.CharField()
    phone      = models.CharField()
    email      = models.CharField()

class Playlist(models.Model):
    owner_username = models.ForeignKey('self') 
    name           = models.CharField()

class PlaylistResource(models.Model):
    RESOURCE_TYPE_CHOICES = (('item'), ('collection'))

    playlist              = models.ForeignKey('Playlist')
    resource_type         = models.CharField(choices=RESOURCE_TYPE_CHOICES)
    resource              = models.IntegerField()

class Location(models.Model):
    TYPE_CHOICES     = (('country'), ('continent'), ('other'))

    name             = models.CharField(primary_key=True)
    type             = models.CharField(choices=TYPE_CHOICES)
    complet_type     = models.ForeignKey('LocationType')
    current_name     = models.ForeignKey('self') 
    is_authoritative = models.BooleanField()

class LocationType(models.Model):
    type = models.CharField()

class LocationAlias(models.Model):
    location_name    = models.ForeignKey('Location')
    alias            = models.CharField()
    is_authoritative = models.BooleanField()
    
class LocationRelation(models.Model):
    location_name        = models.ForeignKey('Location')
    parent_location_name = models.ForeignKey('Location')
    is_authoritative     = models.BooleanField()
    
class ContextKeyword(models.Model):
    value = models.CharField

class MediaItemKeyword(models.Model):
    item    = models.ForeignKey('MediaItem')
    keyword = models.ForeignKey('ContextKeyword')

class Publisher(models.Model): 
    value = models.CharField()

class PublisherCollection(models.Model):
    publisher = models.ForeignKey('Publisher')
    value     = models.CharField()

class Revision(models.Model):
    CHANGE_TYPE_CHOICE = (('create'), ('update'), ('delete'))

    element_type = models.CharField()
    element      = models.ForeignKey('User')
    change_type  = models.CharField(choices=CHANGE_TYPE_CHOICES)
    time         = models.DateTimeField()
    username     = models.ForeignKey('User')
    
class EthnicGroup(models.Model):
    name = models.CharField()

class EthnicGroupAlias(models.Model):
    ethnic_group = models.ForeignKey('EthnicGroup')
    name         = models.CharField()

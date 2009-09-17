from django.db import models

class MediaCollection(models.Model):
    reference               = models.CharField(unique = True)
    physical_format_id      = models.ForeignKey('PhysicalFormat')
    old_code                = models.CharField(unique = True)
    code                    = models.CharField(unique = True)
    title                   = models.CharField()
    alt_title               = models.CharField()
    physical_items_num      = models.IntegerField()
    publishing_status_id    = models.ForeignKey('PublishingStatus')
    creator                 = models.CharField()
    booklet_author          = models.CharField()
    booklet_description     = models.TextField()
    collector               = models.CharField()
    collector_is_creator    = models.BooleanField()
    publisher_id            = models.IntegerField()
    year_published          = models.IntegerField()
    publisher_collection_id = models.ForeignKey('PublisherCollection')   
    publisher_serial        = models.CharField()
    external_references     = models.TextField()
    acquisition_mode_id     = models.ForeignKey('AcquisitionMode')
    comment                 = models.TextField()
    metadata_author_id      = models.ForeignKey('MetadataAuthor')
    metadata_writer_id      = models.ForeignKey('MetadataWriter')
    legal_rights_id         = models.ForeignKey('LegalRight')
    alt_ids                 = models.CharField()
    recorded_from_year      = models.IntegerField()
    recorded_to_year        = models.IntegerField()
    recording_context_id    = models.ForeignKey('RecordingContext')
    approx_duration         = models.TimeField()
    doctype_code            = models.IntegerField()
    travail                 = models.CharField()
    state                   = models.TextField()
    cnrs_contributor        = models.CharField()
    items_done              = models.CharField()
    a_informer_07_03        = models.CharField()
    ad_conversion_id        = models.ForeignKey('AdConversion')
    PUBLIC_ACCESS_CHOICES   = (
        ('none'),
        ('metadata'),
        ('full'),
    )
    public_access           = models.Charfield(choices = PUBLIC_ACCESS_CHOICES) 

class MediaItem(models.Model):
    collection_id       = models.ForeignKey('MediaCollection')
    track               = models.CharField()
    old_code            = models.CharField(unique = True)
    code                = models.CharField(unique = True)
    approx_duration     = models.TimeField()
    recorded_from_date  = models.DateField()
    recorded_to_date    = models.DateField()
    location_name       = models.ForeignKey('Location')
    location_comment    = models.CharField()
    ethnic_group_id     = models.ForeignKey('EthnicGroup')
    title               = models.CharField()
    alt_title           = models.CharField()
    author              = models.CharField()
    vernacular_style_id = models.ForeignKey('VernacularStyle')
    context_comment     = models.TextField()
    external_references = models.TextField()
    moda_execut         = models.CharField()
    copied_from_item_id = models.ForeignKey('self')
    collector           = models.CharField()
    cultural_area       = models.CharField()
    generic_style_id    = models.ForeignKey('GenericStyle')
    collector_selection = models.CharField()
    creator_reference   = models.CharField()
    comment             = models.TextField()
    filename            = models.CharField()
    PUBLIC_ACCESS_CHOICES   = (
        ('none'),
        ('metadata'),
        ('full'),
    )
    public_access           = models.Charfield(choices = PUBLIC_ACCESS_CHOICES)

class MediaPart(models.Model):
    item_id = models.ForeignKey('MediaItem')
    title   = models.CharField()
    start   = models.FloatField()
    end     = models.FloatField()

class PhysicalFormat(models.Model):

class PublishingStatus(models.Model):

class PublisherCollection(models.Model):

class AcquisitionMode(models.Model):

class MetadataAuthor(models.Model):

class MetadataWriter(models.Model):  

class LegalRight(models.Model): 

class RecordingContext(models.Model):

class AdConversion(models.Model):

class EthnicGroup(models.Model):
   
class VernacularStyle(models.Model):

class GenericStyle(models.Model):

class Instrument(models.Model):
    name = models.CharField()

class InstrumentRelation(models.Model):
    instrument_id        = models.ForeignKey('Instrument')
    parent_instrmuent_id = models.ForeignKey('Instrument')

class InstrumentAlias(models.Model):
    name = models.CharField()

class InstrumentAliasRelation(models.Model):
    alias_id      = models.ForeignKey('InstrumentAlias')
    instrument_id = models.ForeignKey('InstrumentAlias')

class MediaItemPerformance(models.Model):
    media_item_id   = models.ForeignKey('MediaItem')
    instrument_id   = models.ForeignKey('Instrument')
    alias_id        = models.ForeignKey('InstrumentAlias')
    instruments_num = models.CharField()
    musicians       = models.CharField()

class User(models.Model):
    username   = models.CharField(primary_key = True)
    LEVEL_CHOICES = (
    ('user'),
    ('maintainer'),
    ('admin'),
    )    
    level      = models.CharField(choices = LEVEL_CHOICES)
    first_name = models.CharField()
    last_name  = models.CharField()
    phone      = models.CharField()
    email      = models.CharField()

class Playlist(models.Model):
    owner_username = models.ForeignKey('self') 
    name           = models.CharField()

class PlaylistResource(models.Model):
    playlist_id   = models.ForeignKey('Playlist')
    RESOURCE_TYPE_CHOICES = (
    ('item'),
    ('collection'),
    )
    resource_type = models.CharField(choices = RESOURCE_TYPE_CHOICES)
    resource_id   = models.ForeignKey('Playlist')

class Location(models.Model):
    name             = models.CharField(primary_key = True)
    TYPE_CHOICES     = (
    ('country'),
    ('continent'),
    ('other'),
    )
    type = models.CharField(choices = TYPE_CHOICES)
    complet_type_id  = models.ForeignKey('LocationType')
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
    item_id    = models.ForeignKey('MediaItem')
    keyword_id = models.ForeignKey('ContextKeyword')

class Publisher(models.Model): 
    value = models.CharField()

class PublisherCollection(models.Model):
    publisher_id = models.ForeignKey('Publisher')
    value        = models.CharField()

class Revision(models.Model):
    element_type = models.CharField()
    element_id   = models.ForeignKey('User')
    CHANGE_TYPE_CHOICE = (
    ('create'),
    ('update'),
    ('delete'),
    )
    change_type  = models.CharField(choices = CHANGE_TYPE_CHOICES)
    time         = models.DateTimeField()
    username     = models.ForeignKey('User')
    
class EthnicGroup(models.Model):
    name = models.CharField()

class EthnicGroupAlias(models.Model):
    name = models.CharField()

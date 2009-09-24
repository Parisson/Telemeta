from django.db import models

class MediaCollection(models.Model):
    "Describe a collection of items"
    PUBLIC_ACCESS_CHOICES = (('0', 'none'), ('1', 'metadata'), ('2', 'full'))

    reference             = models.CharField(unique=True, max_length=250)
    physical_format       = models.ForeignKey('PhysicalFormat', related_name="collections")
    old_code              = models.CharField(unique=True, max_length=250)
    code                  = models.CharField(unique=True, max_length=250)
    title                 = models.CharField(max_length=250)
    alt_title             = models.CharField(max_length=250)
    physical_items_num    = models.IntegerField()
    publishing_status     = models.ForeignKey('PublishingStatus', related_name="collections")
    creator               = models.CharField(max_length=250)
    booklet_author        = models.CharField(max_length=250)
    booklet_description   = models.TextField()
    collector             = models.CharField(max_length=250)
    collector_is_creator  = models.BooleanField()
    publisher             = models.ForeignKey('Publisher', related_name="collections")
    year_published        = models.IntegerField()
    publisher_collection  = models.ForeignKey('PublisherCollection', related_name="collections")
    publisher_serial      = models.CharField(max_length=250)
    external_references   = models.TextField()
    acquisition_mode      = models.ForeignKey('AcquisitionMode', related_name="collections")
    comment               = models.TextField()
    metadata_author       = models.ForeignKey('MetadataAuthor', related_name="collections")
    metadata_writer       = models.ForeignKey('MetadataWriter', related_name="collections")
    legal_rights          = models.ForeignKey('LegalRight', related_name="collections")
    alt_ids               = models.CharField(max_length=250)
    recorded_from_year    = models.IntegerField()
    recorded_to_year      = models.IntegerField()
    recording_context     = models.ForeignKey('RecordingContext', related_name="collections")
    approx_duration       = models.TimeField()
    doctype_code          = models.IntegerField()
    travail               = models.CharField(max_length=250)
    state                 = models.TextField()
    cnrs_contributor      = models.CharField(max_length=250)
    items_done            = models.CharField(max_length=250)
    a_informer_07_03      = models.CharField(max_length=250)
    ad_conversion         = models.ForeignKey('AdConversion', related_name='collections')
    public_access         = models.CharField(choices=PUBLIC_ACCESS_CHOICES, max_length=250)

    class Meta:
        db_table = 'media_collections'

class MediaItem(models.Model):
    "Describe an item"
    PUBLIC_ACCESS_CHOICES = (('0', 'none'), ('1', 'metadata'), ('2', 'full'))

    collection            = models.ForeignKey('MediaCollection', related_name="items")
    track                 = models.CharField(max_length=250)
    old_code              = models.CharField(unique=True, max_length=250)
    code                  = models.CharField(unique=True, max_length=250, null=True)
    approx_duration       = models.TimeField()
    recorded_from_date    = models.DateField()
    recorded_to_date      = models.DateField()
    location_name         = models.ForeignKey('Location', related_name="items",
                                              db_column='location_name')
    location_comment      = models.CharField(max_length=250)
    ethnic_group          = models.ForeignKey('EthnicGroup', related_name="items")
    title                 = models.CharField(max_length=250)
    alt_title             = models.CharField(max_length=250)
    author                = models.CharField(max_length=250)
    vernacular_style      = models.ForeignKey('VernacularStyle', related_name="items")
    context_comment       = models.TextField()
    external_references   = models.TextField()
    moda_execut           = models.CharField(max_length=250)
    copied_from_item      = models.ForeignKey('self', related_name="copies")
    collector             = models.CharField(max_length=250)
    cultural_area         = models.CharField(max_length=250)
    generic_style         = models.ForeignKey('GenericStyle', related_name="items")
    collector_selection   = models.CharField(max_length=250)
    creator_reference     = models.CharField(max_length=250)
    comment               = models.TextField()
    filename              = models.CharField(max_length=250)
    public_access         = models.CharField(choices=PUBLIC_ACCESS_CHOICES, max_length=250)

    class Meta:
        db_table = 'media_items'

class MediaPart(models.Model):
    "Describe an item part"
    item  = models.ForeignKey('MediaItem', related_name="parts")
    title = models.CharField(max_length=250)
    start = models.FloatField()
    end   = models.FloatField()

    class Meta:
        db_table = 'media_parts'

class PhysicalFormat(models.Model):
    "Collection physical format"
    value = models.CharField(max_length=250)
    
    class Meta:
        db_table = 'physical_formats'

class PublishingStatus(models.Model):
    "Collection publishing status"
    value = models.CharField(max_length=250)

    class Meta:
        db_table = 'publishing_status'

class AcquisitionMode(models.Model):
    "Mode of acquisition of the collection"
    value = models.CharField(max_length=250)

    class Meta:
        db_table = 'acquisition_modes'

class MetadataAuthor(models.Model):
    "Collection metadata author"
    value = models.CharField(max_length=250)

    class Meta:
        db_table = 'metadata_authors'

class MetadataWriter(models.Model):  
    "Collection metadata writer"
    value = models.CharField(max_length=250)

    class Meta:
        db_table = 'metadata_writers'

class LegalRight(models.Model):
    "Collection legal rights" 
    value = models.CharField(max_length=250)

    class Meta:
        db_table = 'legal_rights'

class RecordingContext(models.Model):
    "Collection recording context"
    value = models.CharField(max_length=250)

    class Meta:
        db_table = 'recording_contexts'

class AdConversion(models.Model):
    "Collection digital to analog conversion status"
    value = models.CharField(max_length=250)

    class Meta:
        db_table = 'ad_conversions'

class VernacularStyle(models.Model):
    "Item vernacular style"
    value = models.CharField(max_length=250)

    class Meta:
        db_table = 'vernacular_styles'

class GenericStyle(models.Model):
    "Item generic style"
    value = models.CharField(max_length=250)

    class Meta:
        db_table = 'generic_styles'

class Instrument(models.Model):
    "Instrument used in the item"
    name    = models.CharField(max_length=250)

    class Meta:
        db_table = 'instruments'

class InstrumentAlias(models.Model):
    "Instrument other name"
    name = models.CharField(max_length=250)

    class Meta:
        db_table = 'instrument_aliases'

class InstrumentRelation(models.Model):
    "Instrument family"
    instrument        = models.ForeignKey('Instrument', related_name="parent_relation")
    parent_instrument = models.ForeignKey('Instrument', related_name="child_relation")

    class Meta:
        db_table = 'instrument_relations'

class InstrumentAliasRelation(models.Model):
    "Instrument family other name"
    alias      = models.ForeignKey('InstrumentAlias', related_name="other_name")
    instrument = models.ForeignKey('InstrumentAlias', related_name="relation")

    class Meta:
        db_table = 'instrument_alias_relations'

class MediaItemPerformance(models.Model):
    "Item performance"
    media_item      = models.ForeignKey('MediaItem', related_name="performances")
    instrument      = models.ForeignKey('Instrument', related_name="performances",
                                        null=True)
    alias           = models.ForeignKey('InstrumentAlias', related_name="performances",
                                        null=True)
    instruments_num = models.CharField(max_length=250)
    musicians       = models.CharField(max_length=250)

    class Meta:
        db_table = 'media_item_performances'

class User(models.Model):
    "Telemeta user"
    LEVEL_CHOICES = (('0', 'user'), ('1', 'maintainer'), ('2', 'admin'))    

    username   = models.CharField(primary_key=True, max_length=250)
    level      = models.CharField(choices=LEVEL_CHOICES, max_length=250)
    first_name = models.CharField(max_length=250)
    last_name  = models.CharField(max_length=250)
    phone      = models.CharField(max_length=250)
    email      = models.CharField(max_length=250)

    class Meta:
        db_table = 'users'

class Playlist(models.Model):
    "Item or collection playlist"
    owner_username = models.ForeignKey('User', related_name="playlists") 
    name           = models.CharField(max_length=250)

    class Meta:
        db_table = 'playlists'

class PlaylistResource(models.Model):
    "Playlist components"
    RESOURCE_TYPE_CHOICES = (('0', 'item'), ('1', 'collection'))

    playlist              = models.ForeignKey('Playlist', related_name="resources")
    resource_type         = models.CharField(choices=RESOURCE_TYPE_CHOICES, max_length=250)
    resource              = models.IntegerField()

    class Meta:
        db_table = 'playlist_resources'

class Location(models.Model):
    "Item location"
    TYPE_CHOICES     = (('0', 'country'), ('1', 'continent'), ('2', 'other'))

    name             = models.CharField(primary_key=True, max_length=250)
    type             = models.CharField(choices=TYPE_CHOICES, max_length=250)
    complete_type    = models.ForeignKey('LocationType', related_name="types")
    current_name     = models.ForeignKey('self', related_name="past_names", 
                                         db_column="current_name") 
    is_authoritative = models.BooleanField()

    class Meta:
        db_table = 'locations'

class LocationType(models.Model):
    "Location type of an item location"
    id   = models.CharField(max_length=250, primary_key=True)
    name = models.CharField(max_length=250)

    class Meta:
        db_table = 'location_types'

class LocationAlias(models.Model):
    "Location other name"
    location_name    = models.ForeignKey('Location', related_name="aliases",
                                          db_column="location_name")
    alias            = models.CharField(max_length=250)
    is_authoritative = models.BooleanField()

    class Meta:
        db_table = 'location_aliases'
    
class LocationRelation(models.Model):
    "Location family"
    location_name        = models.ForeignKey('Location', related_name="parent_relations",
                                              db_column="location_name")
    parent_location_name = models.ForeignKey('Location', related_name="child_relations",
                                              db_column="parent_location_name")
    is_authoritative     = models.BooleanField()

    class Meta:
        db_table = 'location_relations'
    
class ContextKeyword(models.Model):
    "Keyword"
    value = models.CharField(max_length=250)

    class Meta:
        db_table = 'context_keywords'

class MediaItemKeyword(models.Model):
    "Item keyword"
    item    = models.ForeignKey('MediaItem', related_name="items")
    keyword = models.ForeignKey('ContextKeyword', related_name="keywords")

    class Meta:
        db_table = 'media_item_keywords'

class Publisher(models.Model): 
    "Collection publisher"
    value = models.CharField(max_length=250)

    class Meta:
        db_table = 'publishers'

class PublisherCollection(models.Model):
    "Collection which belongs to publisher"
    publisher = models.ForeignKey('Publisher', related_name="publisher_collections")
    value     = models.CharField(max_length=250)

    class Meta:
        db_table = 'publisher_collections'

class Revision(models.Model):
    "Revision made by user"
    CHANGE_TYPE_CHOICES = (('0', 'create'), ('1', 'update'), ('2','delete'))

    element_type        = models.CharField(max_length=250)
    element_id          = models.IntegerField()
    change_type         = models.CharField(choices=CHANGE_TYPE_CHOICES, max_length=250)
    time                = models.DateTimeField()
    username            = models.ForeignKey('User', related_name="usernames")

    class Meta:
        db_table = 'revisions'
    
class EthnicGroup(models.Model):
    "Item ethnic group"
    name = models.CharField(max_length=250)

    class Meta:
        db_table = 'ethnic_groups'

class EthnicGroupAlias(models.Model):
    "Item ethnic group other name" 
    ethnic_group = models.ForeignKey('EthnicGroup', related_name="aliases")
    name         = models.CharField(max_length=250)

    class Meta:
        db_table = 'ethnic_group_aliases'        

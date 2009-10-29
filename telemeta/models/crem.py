# -*- coding: utf-8 -*-
# Copyright (C) 2007 Samalyse SARL

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
# Authors: Olivier Guilyardi <olivier@samalyse.com>
#          David LIPSZYC <davidlipszyc@gmail.com>

from django.db import models
import query

class MediaCollection(models.Model):
    "Describe a collection of items"
    PUBLIC_ACCESS_CHOICES = (('none', 'none'), ('metadata', 'metadata'), ('metadata', 'full'))

    reference             = models.CharField(unique=True, max_length=250,
                                             null=True)
    physical_format       = models.ForeignKey('PhysicalFormat', related_name="collections", 
                                              null=True)
    old_code              = models.CharField(unique=True, max_length=250)
    code                  = models.CharField(unique=True, max_length=250)
    title                 = models.CharField(max_length=250)
    alt_title             = models.CharField(max_length=250, default="")
    physical_items_num    = models.IntegerField(default=0)
    publishing_status     = models.ForeignKey('PublishingStatus', related_name="collections",
                                              null=True)
    creator               = models.CharField(max_length=250, default="")
    booklet_author        = models.CharField(max_length=250, default="")
    booklet_description   = models.TextField(default="")
    collector             = models.CharField(max_length=250, default="")
    collector_is_creator  = models.BooleanField(default="")
    publisher             = models.ForeignKey('Publisher', related_name="collections",
                                              null=True)     
    year_published        = models.IntegerField(default=0)
    publisher_collection  = models.ForeignKey('PublisherCollection', related_name="collections",
                                              null=True)
    publisher_serial      = models.CharField(max_length=250, default="")
    external_references   = models.TextField(default="")
    acquisition_mode      = models.ForeignKey('AcquisitionMode', related_name="collections",
                                              null=True)
    comment               = models.TextField(default="")
    metadata_author       = models.ForeignKey('MetadataAuthor', related_name="collections",
                                              null=True)
    metadata_writer       = models.ForeignKey('MetadataWriter', related_name="collections",
                                              null=True)
    legal_rights          = models.ForeignKey('LegalRight', related_name="collections",
                                              null=True)
    alt_ids               = models.CharField(max_length=250, default="")
    recorded_from_year    = models.IntegerField(default=0)
    recorded_to_year      = models.IntegerField(default=0)
    recording_context     = models.ForeignKey('RecordingContext', related_name="collections",
                                              null=True)
    approx_duration       = models.TimeField(default=0)
    doctype_code          = models.IntegerField(default=0)
    travail               = models.CharField(max_length=250, default="")
    state                 = models.TextField(default="")
    cnrs_contributor      = models.CharField(max_length=250, default="")
    items_done            = models.CharField(max_length=250, default="")
    a_informer_07_03      = models.CharField(max_length=250, default="")
    ad_conversion         = models.ForeignKey('AdConversion', related_name='collections',
                                              null=True)
    public_access         = models.CharField(choices=PUBLIC_ACCESS_CHOICES, max_length=250, default="metadata")

    objects               = query.MediaCollectionManager()

    def __unicode__(self):
        return self.code

    def save(self, force_insert=False, force_update=False):
        raise MissingUserError("save() method disabled, use save_by_user()")

    def save_by_user(self, user, force_insert=False, force_update=False):
        "Save a collection and add a revision"
        super(MediaCollection, self).save(force_insert, force_update)
        Revision(element_type='collection', element_id=self.id, user=user).touch()    

    class Meta:
        db_table = 'media_collections'

class MediaItem(models.Model):
    "Describe an item"
    PUBLIC_ACCESS_CHOICES = (('none', 'none'), ('metadata', 'metadata'), ('full', 'full'))

    collection            = models.ForeignKey('MediaCollection', related_name="items")
    track                 = models.CharField(max_length=250, default="")
    old_code              = models.CharField(unique=True, max_length=250)
    code                  = models.CharField(unique=True, max_length=250, null=True)
    approx_duration       = models.TimeField(default=0)
    recorded_from_date    = models.DateField(default=0)
    recorded_to_date      = models.DateField(default=0)
    location_name         = models.ForeignKey('Location', related_name="items",
                                              db_column='location_name', null=True, default="")
    location_comment      = models.CharField(max_length=250, default="")
    ethnic_group          = models.ForeignKey('EthnicGroup', related_name="items",
                                              null=True)
    title                 = models.CharField(max_length=250)
    alt_title             = models.CharField(max_length=250, default="")
    author                = models.CharField(max_length=250, default="")
    vernacular_style      = models.ForeignKey('VernacularStyle', related_name="items",
                                              null=True)
    context_comment       = models.TextField(default="")
    external_references   = models.TextField(default="")
    moda_execut           = models.CharField(max_length=250, default="")
    copied_from_item      = models.ForeignKey('self', related_name="copies",
                                              null=True)
    collector             = models.CharField(max_length=250, default="")
    cultural_area         = models.CharField(max_length=250, default="")
    generic_style         = models.ForeignKey('GenericStyle', related_name="items",
                                              null=True)
    collector_selection   = models.CharField(max_length=250, default="")
    creator_reference     = models.CharField(max_length=250, default="")
    comment               = models.TextField(default="")
    filename              = models.CharField(max_length=250, default="")
    public_access         = models.CharField(choices=PUBLIC_ACCESS_CHOICES, 
                                             max_length=250, default="metadata")

    objects               = query.MediaItemManager()

    class Meta:
        db_table = 'media_items'

    def __unicode__(self):
        if self.code:
            return self.code
        return self.old_code

    def save(self, force_insert=False, force_update=False):
        raise MissingUserError("save() method disabled, use save_by_user()")

    def save_by_user(self, user, force_insert=False, force_update=False):
        "Save an item and add a revision"
        super(MediaItem, self).save(force_insert, force_update)
        Revision(element_type='item', element_id=self.id, user=user).touch()    

class MediaPart(models.Model):
    "Describe an item part"
    item  = models.ForeignKey('MediaItem', related_name="parts")
    title = models.CharField(max_length=250)
    start = models.FloatField()
    end   = models.FloatField()
    
    class Meta:
        db_table = 'media_parts'

    def __unicode__(self):
        return self.title

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
    instruments_num = models.CharField(max_length=250, default="")
    musicians       = models.CharField(max_length=250, default="")

    class Meta:
        db_table = 'media_item_performances'

class User(models.Model):
    "Telemeta user"
    LEVEL_CHOICES = (('user', 'user'), ('maintainer', 'maintainer'), ('admin', 'admin'))    

    username   = models.CharField(primary_key=True, max_length=250)
    level      = models.CharField(choices=LEVEL_CHOICES, max_length=250)
    first_name = models.CharField(max_length=250, default="")
    last_name  = models.CharField(max_length=250, default="")
    phone      = models.CharField(max_length=250, default="")
    email      = models.CharField(max_length=250, default="")

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
    RESOURCE_TYPE_CHOICES = (('item', 'item'), ('collection', 'collection'))

    playlist              = models.ForeignKey('Playlist', related_name="resources")
    resource_type         = models.CharField(choices=RESOURCE_TYPE_CHOICES, max_length=250)
    resource              = models.IntegerField()

    class Meta:
        db_table = 'playlist_resources'

class Location(models.Model):
    "Item location"
    TYPE_CHOICES     = (('country', 'country'), ('continent', 'continent'), ('other', 'other'))

    name             = models.CharField(primary_key=True, max_length=250)
    type             = models.CharField(choices=TYPE_CHOICES, max_length=250)
    complete_type    = models.ForeignKey('LocationType', related_name="types")
    current_name     = models.ForeignKey('self', related_name="past_names", 
                                         db_column="current_name", null=True) 
    is_authoritative = models.BooleanField(default=0)

    class Meta:
        db_table = 'locations'

    def __unicode__(self):
        return self.name

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
    is_authoritative = models.BooleanField(default=0)

    class Meta:
        db_table = 'location_aliases'
    
class LocationRelation(models.Model):
    "Location family"
    location_name        = models.ForeignKey('Location', related_name="parent_relations",
                                              db_column="location_name")
    parent_location_name = models.ForeignKey('Location', related_name="child_relations",
                                              db_column="parent_location_name", null=True)
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
    item    = models.ForeignKey('MediaItem')
    keyword = models.ForeignKey('ContextKeyword')

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
    ELEMENT_TYPE_CHOICES = (('collection', 'collection'), ('item', 'item'), ('part', 'part'))
    CHANGE_TYPE_CHOICES  = (('import', 'import'), ('create', 'create'), ('update', 'update'), ('delete','delete'))

    element_type         = models.CharField(choices=ELEMENT_TYPE_CHOICES, max_length=250)
    element_id           = models.IntegerField()
    change_type          = models.CharField(choices=CHANGE_TYPE_CHOICES, max_length=250)
    time                 = models.DateTimeField(auto_now_add=True)
    user                 = models.ForeignKey('User', db_column='username', related_name="revisions")
    
    def touch(self):    
        "Create or update a revision"
        q = Revision.objects.filter(element_type=self.element_type, element_id=self.element_id)
        if q.count():
            self.change_type = 'update'
        else:
            self.change_type = 'create'
        self.save()

    class Meta:
        db_table = 'revisions'
    
class EthnicGroup(models.Model):
    "Item ethnic group"
    name = models.CharField(max_length=250)

    class Meta:
        db_table = 'ethnic_groups'

    def __unicode__(self):
        return self.name

class EthnicGroupAlias(models.Model):
    "Item ethnic group other name" 
    ethnic_group = models.ForeignKey('EthnicGroup', related_name="aliases")
    name         = models.CharField(max_length=250)

    class Meta:
        db_table = 'ethnic_group_aliases'


class MissingUserError(Exception):
    pass

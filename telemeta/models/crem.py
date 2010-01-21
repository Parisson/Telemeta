# -*- coding: utf-8 -*-
# Copyright (C) 2007-2010 Samalyse SARL

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
from django.core.exceptions import ObjectDoesNotExist
import cremquery as query
from xml.dom.minidom import getDOMImplementation
from telemeta.util.unaccent import unaccent_icmp
import re
from telemeta.models.core import DurationField, Duration
from telemeta.models import dublincore as dc

class ModelCore(models.Model):

    @classmethod
    def required_fields(cls):
        required = []
        for field in cls._meta.fields:
            if (field != cls._meta.pk and field.default == models.fields.NOT_PROVIDED and
                    not field.null and not getattr(field, 'auto_now_add', False)):
                required.append(field)
        return required

    def save(self, force_insert=False, force_update=False, using=None):
        required = self.required_fields()
        for field in required:
            if not getattr(self, field.name):
                raise RequiredFieldError(self, field)
        super(ModelCore, self).save(force_insert, force_update, using)

    class Meta:
        abstract = True

class MediaResource(ModelCore):
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

    @classmethod
    def get_dom_name(cls):
        "Convert the class name to a DOM element name"
        clsname = cls.__name__
        return clsname[0].lower() + clsname[1:]

    @staticmethod
    def get_dom_field_name(field_name):
        "Convert the class name to a DOM element name"
        tokens = field_name.split('_')
        name = tokens[0]
        for t in tokens[1:]:
            name += t[0].upper() + t[1:]
        return name

    def to_dom(self):
        "Return the DOM representation of this media object"
        impl = getDOMImplementation()
        root = self.get_dom_name()
        doc = impl.createDocument(None, root, None)
        top = doc.documentElement
        top.setAttribute("id", str(self.id))
        fields = self.to_dict()
        for name, value in fields.iteritems():
            element = doc.createElement(self.get_dom_field_name(name))
            if isinstance(value, models.Model):
                element.setAttribute('key', str(value.pk))
            value = unicode(value)
            element.appendChild(doc.createTextNode(value))
            top.appendChild(element)
        return doc
    
    def save_with_revision(self, user, force_insert=False, force_update=False, using=None):
        "Save a media object and add a revision"
        self.save(force_insert, force_update, using)
        Revision.touch(self, user)    

    def get_revision(self):
        return Revision.objects.filter(element_type=self.element_type, element_id=self.id).order_by('-time')[0]

    def dc_access_rights(self):
        if self.public_access == 'full':
            return 'public'
        if self.public_access == 'metadata':
            return 'restricted'
        return 'private'

    def dc_identifier(self):
        if self.code:
            return self.element_type + ':' + self.code
        elif self.old_code:
            return self.element_type + ':' + self.old_code
        return None

    class Meta:
        abstract = True

class MetaCore:
    app_label = 'telemeta'

class MediaCollection(MediaResource):
    "Describe a collection of items"
    element_type = 'collection'
    PUBLIC_ACCESS_CHOICES = (('none', 'none'), ('metadata', 'metadata'), ('metadata', 'full'))

    reference             = models.CharField(unique=True, max_length=250,
                                             null=True)
    physical_format       = models.ForeignKey('PhysicalFormat', related_name="collections", 
                                              null=True)
    old_code              = models.CharField(unique=True, max_length=250, null=True)
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
    is_published          = models.BooleanField(default="")
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
    approx_duration       = DurationField(default='00:00')
    doctype_code          = models.IntegerField(default=0)
    travail               = models.CharField(max_length=250, default="")
    state                 = models.TextField(default="")
    cnrs_contributor      = models.CharField(max_length=250, default="")
    items_done            = models.CharField(max_length=250, default="")
    a_informer_07_03      = models.CharField(max_length=250, default="")
    ad_conversion         = models.ForeignKey('AdConversion', related_name='collections',
                                              null=True)
    public_access         = models.CharField(choices=PUBLIC_ACCESS_CHOICES, max_length=16, default="metadata")

    objects               = query.MediaCollectionManager()

    def __unicode__(self):
        return self.code

    def has_mediafile(self):
        "Tell wether this collection has any media files attached to its items"
        items = self.items.all()
        for item in items:
            if item.file:
                return True
        return False

    def __name_cmp(self, obj1, obj2):
        return unaccent_icmp(obj1.name, obj2.name)

    def get_countries(self):
        "Return the countries of the items"
        countries = []
        items = self.items.all()
        for item in items:
            if item.location:
                country = item.location.country()
                if country and not country in countries:
                    countries.append(country)

        countries.sort(self.__name_cmp)                

        return countries

    def get_ethnic_groups(self):
        "Return the ethnic groups of the items"
        groups = []
        items = self.items.all()
        for item in items:
            if item.ethnic_group and not item.ethnic_group in groups:
                groups.append(item.ethnic_group)

        groups.sort(self.__name_cmp)                

        return groups

    def is_valid_code(self, code):
        "Check if the collection code is well formed"
        if self.is_published:
            regex = '^CNRSMH_E_[0-9]{4}_[0-9]{3}_[0-9]{3}$'
        else:
            regex = '^CNRSMH_I_[0-9]{4}_[0-9]{3}$'
           
        if re.match(regex, code):
            return True

        return False

    def save(self, force_insert=False, force_update=False, using=None):
        if not self.code:
            raise RequiredFieldError(self, self._meta.get_field('code'))
        if not self.is_valid_code(self.code):
            raise MediaInvalidCodeError("%s is not a valid code for this collection" % self.code)
        super(MediaCollection, self).save(force_insert, force_update, using)

    def to_dublincore(self):
        "Express this collection as a Dublin Core resource"

        if self.collector:
            creator = (dc.Element('creator', self.collector), 
                       dc.Element('contributor', self.creator))
        else:                        
            creator = dc.Element('creator', self.creator)

        resource = dc.Resource(
            dc.Element('identifier',  self.dc_identifier()),
            dc.Element('type',        'Collection'),
            dc.Element('title',       self.title),
            dc.Element('title',       self.alt_title),
            creator,
            dc.Element('contributor', self.metadata_author),
            dc.Element('subject',     'Ethnologie'),
            dc.Element('subject',     'Ethnomusicologie'),
            dc.Element('publisher',   self.publisher),
            dc.Element('publisher',   u'CNRS - Musée de l\'homme'),
            dc.Date(self.recorded_from_year, self.recorded_to_year, 'created'),
            dc.Date(self.year_published, refinement='issued'),
            dc.Element('rightsHolder', self.creator),
            dc.Element('rightsHolder', self.collector),
            dc.Element('rightsHolder', self.publisher),
        )
           
        duration = Duration()
        parts = []
        for item in self.items.all():
            duration += item.duration()

            id = item.dc_identifier()
            if id:
                parts.append(dc.Element('relation', id, 'hasPart'))

        if duration < self.approx_duration:            
            duration = self.approx_duration

        resource.add(
            dc.Element('rights', self.legal_rights, 'license'),
            dc.Element('rights', self.dc_access_rights(), 'accessRights'),
            dc.Element('format', duration, 'extent'),
            dc.Element('format', self.physical_format, 'medium'),
            #FIXME: audio mime types are missing,
            parts
        )

        return resource

    class Meta(MetaCore):
        db_table = 'media_collections'

class MediaItem(MediaResource):
    "Describe an item"
    element_type = 'item'
    PUBLIC_ACCESS_CHOICES = (('none', 'none'), ('metadata', 'metadata'), ('full', 'full'))

    collection            = models.ForeignKey('MediaCollection', related_name="items")
    track                 = models.CharField(max_length=250, default="")
    old_code              = models.CharField(unique=True, max_length=250, null=True)
    code                  = models.CharField(unique=True, max_length=250, null=True)
    approx_duration       = DurationField(default='00:00')
    recorded_from_date    = models.DateField(default=0)
    recorded_to_date      = models.DateField(default=0)
    location              = models.ForeignKey('Location', related_name="items",
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
    file                  = models.FileField(upload_to='items/%Y/%m/%d', db_column="filename", default='')
    public_access         = models.CharField(choices=PUBLIC_ACCESS_CHOICES, 
                                             max_length=16, default="metadata")

    objects               = query.MediaItemManager()

    class Meta(MetaCore):
        db_table = 'media_items'

    def is_valid_code(self, code):
        "Check if the item code is well formed"
        if self.collection.is_published:
            regex = '^' + self.collection.code + '_[0-9]{2}(_[0-9]{2})?$'
        else:
            regex = '^' + self.collection.code + '_[0-9]{3}(_[0-9]{2})?(_[0-9]{2})?$'

        if re.match(regex, self.code):
            return True

        return False

    def save(self, force_insert=False, force_update=False, using=None):
        if not self.code:
            raise RequiredFieldError(self, self._meta.get_field('code'))
        if not self.is_valid_code(self.code):
            raise MediaInvalidCodeError("%s is not a valid item code for collection %s" 
                                        % (self.code, self.collection.code))
        super(MediaItem, self).save(force_insert, force_update, using)

    def duration(self):
        "Tell the length in seconds of this item media data"
        # FIXME: use TimeSide?
        seconds = 0
        if self.file:
            import wave
            media = wave.open(self.file.path, "rb")
            seconds = media.getnframes() / media.getframerate()
            media.close()

        if seconds:
            return Duration(seconds=seconds)

        return self.approx_duration

    def __unicode__(self):
        if self.code:
            return self.code
        return self.old_code

class MediaPart(MediaResource):
    "Describe an item part"
    element_type = 'part'
    item  = models.ForeignKey('MediaItem', related_name="parts")
    title = models.CharField(max_length=250)
    start = models.FloatField()
    end   = models.FloatField()
    
    class Meta(MetaCore):
        db_table = 'media_parts'

    def __unicode__(self):
        return self.title

class Enumeration(ModelCore):
    "Abstract enumerations base class"
    value = models.CharField(max_length=250, unique=True)
    
    def __unicode__(self):
        return self.value

    class Meta(MetaCore):
        abstract = True

class PhysicalFormat(Enumeration):
    "Collection physical format"

    class Meta(MetaCore):
        db_table = 'physical_formats'

class PublishingStatus(Enumeration):
    "Collection publishing status"

    class Meta(MetaCore):
        db_table = 'publishing_status'

class AcquisitionMode(Enumeration):
    "Mode of acquisition of the collection"

    class Meta(MetaCore):
        db_table = 'acquisition_modes'

class MetadataAuthor(Enumeration):
    "Collection metadata author"

    class Meta(MetaCore):
        db_table = 'metadata_authors'

class MetadataWriter(Enumeration):  
    "Collection metadata writer"

    class Meta(MetaCore):
        db_table = 'metadata_writers'

class LegalRight(Enumeration):
    "Collection legal rights" 

    class Meta(MetaCore):
        db_table = 'legal_rights'

class RecordingContext(Enumeration):
    "Collection recording context"

    class Meta(MetaCore):
        db_table = 'recording_contexts'

class AdConversion(Enumeration):
    "Collection digital to analog conversion status"

    class Meta(MetaCore):
        db_table = 'ad_conversions'

class VernacularStyle(Enumeration):
    "Item vernacular style"

    class Meta(MetaCore):
        db_table = 'vernacular_styles'

class GenericStyle(Enumeration):
    "Item generic style"

    class Meta(MetaCore):
        db_table = 'generic_styles'

class Instrument(ModelCore):
    "Instrument used in the item"
    name    = models.CharField(max_length=250)

    class Meta(MetaCore):
        db_table = 'instruments'

    def __unicode__(self):
        return self.name

class InstrumentAlias(ModelCore):
    "Instrument other name"
    name = models.CharField(max_length=250)

    class Meta(MetaCore):
        db_table = 'instrument_aliases'

    def __unicode__(self):
        return self.name

class InstrumentRelation(ModelCore):
    "Instrument family"
    instrument        = models.ForeignKey('Instrument', related_name="parent_relation")
    parent_instrument = models.ForeignKey('Instrument', related_name="child_relation")

    class Meta(MetaCore):
        db_table = 'instrument_relations'
        unique_together = (('instrument', 'parent_instrument'),)

class InstrumentAliasRelation(ModelCore):
    "Instrument family other name"
    alias      = models.ForeignKey('InstrumentAlias', related_name="other_name")
    instrument = models.ForeignKey('InstrumentAlias', related_name="relation")

    class Meta(MetaCore):
        db_table = 'instrument_alias_relations'
        unique_together = (('alias', 'instrument'),)

class MediaItemPerformance(ModelCore):
    "Item performance"
    media_item      = models.ForeignKey('MediaItem', related_name="performances")
    instrument      = models.ForeignKey('Instrument', related_name="performances",
                                        null=True)
    alias           = models.ForeignKey('InstrumentAlias', related_name="performances",
                                        null=True)
    instruments_num = models.CharField(max_length=250, default="")
    musicians       = models.CharField(max_length=250, default="")

    class Meta(MetaCore):
        db_table = 'media_item_performances'

class User(ModelCore):
    "Telemeta user"
    LEVEL_CHOICES = (('user', 'user'), ('maintainer', 'maintainer'), ('admin', 'admin'))    

    username   = models.CharField(primary_key=True, max_length=64)
    level      = models.CharField(choices=LEVEL_CHOICES, max_length=250)
    first_name = models.CharField(max_length=250, default="")
    last_name  = models.CharField(max_length=250, default="")
    phone      = models.CharField(max_length=250, default="")
    email      = models.CharField(max_length=250, default="")

    class Meta(MetaCore):
        db_table = 'users'

    def __unicode__(self):
        return self.username

class Playlist(ModelCore):
    "Item or collection playlist"
    owner_username = models.ForeignKey('User', related_name="playlists", db_column="owner_username") 
    name           = models.CharField(max_length=250)

    class Meta(MetaCore):
        db_table = 'playlists'

    def __unicode__(self):
        return self.name

class PlaylistResource(ModelCore):
    "Playlist components"
    RESOURCE_TYPE_CHOICES = (('item', 'item'), ('collection', 'collection'))

    playlist              = models.ForeignKey('Playlist', related_name="resources")
    resource_type         = models.CharField(choices=RESOURCE_TYPE_CHOICES, max_length=250)
    resource              = models.IntegerField()

    class Meta(MetaCore):
        db_table = 'playlist_resources'

class Location(ModelCore):
    "Item location"
    TYPE_CHOICES     = (('country', 'country'), ('continent', 'continent'), ('other', 'other'))

    name             = models.CharField(primary_key=True, max_length=150)
    type             = models.CharField(choices=TYPE_CHOICES, max_length=16)
    complete_type    = models.ForeignKey('LocationType', related_name="types")
    current_name     = models.ForeignKey('self', related_name="past_names", 
                                         db_column="current_name", null=True) 
    is_authoritative = models.BooleanField(default=0)

    def _by_type(self, typename):
        location = self
        while location.type != typename:
            relations = location.parent_relations
            if relations:
                location = relations.all()[0].parent_location
            else:
                location = None
                break

        return location

    def country(self):
        return self._by_type('country')

    def continent(self):
        return self._by_type('continent')

    class Meta(MetaCore):
        db_table = 'locations'

    def __unicode__(self):
        return self.name

class LocationType(ModelCore):
    "Location type of an item location"
    id   = models.CharField(max_length=64, primary_key=True)
    name = models.CharField(max_length=150)

    class Meta(MetaCore):
        db_table = 'location_types'

class LocationAlias(ModelCore):
    "Location other name"
    location         = models.ForeignKey('Location', related_name="aliases",
                                          db_column="location_name", max_length=150)
    alias            = models.CharField(max_length=150)
    is_authoritative = models.BooleanField(default=0)

    def __unicode__(self):
        return self.alias

    class Meta(MetaCore):
        db_table = 'location_aliases'
        unique_together = (('location', 'alias'),)
    
class LocationRelation(ModelCore):
    "Location family"
    location             = models.ForeignKey('Location', related_name="parent_relations",
                                              db_column="location_name", max_length=150)
    parent_location      = models.ForeignKey('Location', related_name="child_relations",
                                              db_column="parent_location_name", null=True, max_length=150)
    is_authoritative     = models.BooleanField()

    class Meta(MetaCore):
        db_table = 'location_relations'
    
class ContextKeyword(Enumeration):
    "Keyword"

    class Meta(MetaCore):
        db_table = 'context_keywords'

class MediaItemKeyword(ModelCore):
    "Item keyword"
    item    = models.ForeignKey('MediaItem')
    keyword = models.ForeignKey('ContextKeyword')

    class Meta(MetaCore):
        db_table = 'media_item_keywords'
        unique_together = (('item', 'keyword'),)

class Publisher(Enumeration): 
    "Collection publisher"

    class Meta(MetaCore):
        db_table = 'publishers'

class PublisherCollection(ModelCore):
    "Collection which belongs to publisher"
    publisher = models.ForeignKey('Publisher', related_name="publisher_collections")
    value     = models.CharField(max_length=250)

    def __unicode__(self):
        return self.value

    class Meta(MetaCore):
        db_table = 'publisher_collections'

class Revision(ModelCore):
    "Revision made by user"
    ELEMENT_TYPE_CHOICES = (('collection', 'collection'), ('item', 'item'), ('part', 'part'))
    CHANGE_TYPE_CHOICES  = (('import', 'import'), ('create', 'create'), ('update', 'update'), ('delete','delete'))

    element_type         = models.CharField(choices=ELEMENT_TYPE_CHOICES, max_length=16)
    element_id           = models.IntegerField()
    change_type          = models.CharField(choices=CHANGE_TYPE_CHOICES, max_length=16)
    time                 = models.DateTimeField(auto_now_add=True)
    user                 = models.ForeignKey('User', db_column='username', related_name="revisions")
    
    @classmethod
    def touch(cls, element, user):    
        "Create or update a revision"
        revision = cls(element_type=element.element_type, element_id=element.pk, 
                       user=user, change_type='create')
        if element.pk:
            try: 
                element.__class__.objects.get(pk=element.pk)
            except ObjectDoesNotExist:
                pass
            else:
                revision.change_type = 'update'

        revision.save()
        return revision

    class Meta(MetaCore):
        db_table = 'revisions'
    
class EthnicGroup(ModelCore):
    "Item ethnic group"
    name = models.CharField(max_length=250)

    class Meta(MetaCore):
        db_table = 'ethnic_groups'

    def __unicode__(self):
        return self.name

class EthnicGroupAlias(ModelCore):
    "Item ethnic group other name" 
    ethnic_group = models.ForeignKey('EthnicGroup', related_name="aliases")
    name         = models.CharField(max_length=250)

    class Meta(MetaCore):
        db_table = 'ethnic_group_aliases'


class MissingUserError(Exception):
    pass

class RequiredFieldError(Exception):
    def __init__(self, model, field):
        self.model = model
        self.field = field
        super(Exception, self).__init__('%s.%s is required' % (model._meta.object_name, field.name))

class MediaInvalidCodeError(Exception):
    pass

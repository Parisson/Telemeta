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
import cremquery as query
from xml.dom.minidom import getDOMImplementation
from telemeta.util.unaccent import unaccent_icmp

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

class MediaCore(ModelCore):
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
    
    def is_well_formed_id(cls, value):
        "Check if the media id is well formed"
        regex = re.compile(r"^" + media_id_regex + r"$")
        if regex.match(value):
            return True 
        else:
            return False
    is_well_formed_id = classmethod(is_well_formed_id)

    def save(self, force_insert=False, force_update=False, using=None):
        raise MissingUserError("save() method disabled, use save_by_user()")

    def save_by_user(self, user, force_insert=False, force_update=False, using=None):
        "Save a media object and add a revision"
        super(MediaCore, self).save(force_insert, force_update, using)
        Revision(element_type=self.element_type, element_id=self.id, user=user).touch()    

    def get_revision(self):
        return Revision.objects.filter(element_type=self.element_type, element_id=self.id).order_by('-time')[0]

    class Meta:
        abstract = True

class MetaCore:
    app_label = 'telemeta'

class MediaCollection(MediaCore):
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
    approx_duration       = models.TimeField(default='00:00')
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

    class Meta(MetaCore):
        db_table = 'media_collections'

class MediaItem(MediaCore):
    "Describe an item"
    element_type = 'item'
    PUBLIC_ACCESS_CHOICES = (('none', 'none'), ('metadata', 'metadata'), ('full', 'full'))

    collection            = models.ForeignKey('MediaCollection', related_name="items")
    track                 = models.CharField(max_length=250, default="")
    old_code              = models.CharField(unique=True, max_length=250, null=True)
    code                  = models.CharField(unique=True, max_length=250, null=True)
    approx_duration       = models.TimeField(default='00:00')
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

    def __unicode__(self):
        if self.code:
            return self.code
        return self.old_code

class MediaPart(MediaCore):
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

class PhysicalFormat(ModelCore):
    "Collection physical format"
    value = models.CharField(max_length=250, unique=True)
    
    class Meta(MetaCore):
        db_table = 'physical_formats'

class PublishingStatus(ModelCore):
    "Collection publishing status"
    value = models.CharField(max_length=250, unique=True)

    class Meta(MetaCore):
        db_table = 'publishing_status'

class AcquisitionMode(ModelCore):
    "Mode of acquisition of the collection"
    value = models.CharField(max_length=250, unique=True)

    class Meta(MetaCore):
        db_table = 'acquisition_modes'

class MetadataAuthor(ModelCore):
    "Collection metadata author"
    value = models.CharField(max_length=250, unique=True)

    class Meta(MetaCore):
        db_table = 'metadata_authors'

class MetadataWriter(ModelCore):  
    "Collection metadata writer"
    value = models.CharField(max_length=250, unique=True)

    class Meta(MetaCore):
        db_table = 'metadata_writers'

class LegalRight(ModelCore):
    "Collection legal rights" 
    value = models.CharField(max_length=250, unique=True)

    class Meta(MetaCore):
        db_table = 'legal_rights'

class RecordingContext(ModelCore):
    "Collection recording context"
    value = models.CharField(max_length=250, unique=True)

    class Meta(MetaCore):
        db_table = 'recording_contexts'

class AdConversion(ModelCore):
    "Collection digital to analog conversion status"
    value = models.CharField(max_length=250, unique=True)

    class Meta(MetaCore):
        db_table = 'ad_conversions'

class VernacularStyle(ModelCore):
    "Item vernacular style"
    value = models.CharField(max_length=250, unique=True)

    class Meta(MetaCore):
        db_table = 'vernacular_styles'

class GenericStyle(ModelCore):
    "Item generic style"
    value = models.CharField(max_length=250, unique=True)

    class Meta(MetaCore):
        db_table = 'generic_styles'

class Instrument(ModelCore):
    "Instrument used in the item"
    name    = models.CharField(max_length=250)

    class Meta(MetaCore):
        db_table = 'instruments'

class InstrumentAlias(ModelCore):
    "Instrument other name"
    name = models.CharField(max_length=250)

    class Meta(MetaCore):
        db_table = 'instrument_aliases'

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

class Playlist(ModelCore):
    "Item or collection playlist"
    owner_username = models.ForeignKey('User', related_name="playlists", db_column="owner_username") 
    name           = models.CharField(max_length=250)

    class Meta(MetaCore):
        db_table = 'playlists'

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
    
class ContextKeyword(ModelCore):
    "Keyword"
    value = models.CharField(max_length=250)

    class Meta(MetaCore):
        db_table = 'context_keywords'

class MediaItemKeyword(ModelCore):
    "Item keyword"
    item    = models.ForeignKey('MediaItem')
    keyword = models.ForeignKey('ContextKeyword')

    class Meta(MetaCore):
        db_table = 'media_item_keywords'
        unique_together = (('item', 'keyword'),)

class Publisher(ModelCore): 
    "Collection publisher"
    value = models.CharField(max_length=250, unique=True)

    class Meta(MetaCore):
        db_table = 'publishers'

class PublisherCollection(ModelCore):
    "Collection which belongs to publisher"
    publisher = models.ForeignKey('Publisher', related_name="publisher_collections")
    value     = models.CharField(max_length=250)

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
    
    def touch(self):    
        "Create or update a revision"
        q = Revision.objects.filter(element_type=self.element_type, element_id=self.element_id)
        if q.count():
            self.change_type = 'update'
        else:
            self.change_type = 'create'
        self.save()

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

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

from django.core.exceptions import ObjectDoesNotExist
import cremquery as query
from xml.dom.minidom import getDOMImplementation
from telemeta.util.unaccent import unaccent_icmp
import re
from django.db.models import FieldDoesNotExist
from telemeta.models.core import DurationField, Duration, WeakForeignKey, EnhancedModel, \
                                 CharField, TextField, IntegerField, BooleanField, \
                                 DateTimeField, FileField, ForeignKey, FloatField, DateField
from telemeta.models import dublincore as dc
from django.utils.translation import ugettext_lazy as _

class ModelCore(EnhancedModel):

    @classmethod
    def required_fields(cls):
        required = []
        for field in cls._meta.fields:
            if not field.blank:
                required.append(field)
        return required

    def save(self, force_insert=False, force_update=False, using=None):
        required = self.required_fields()
        for field in required:
            if not getattr(self, field.name):
                raise RequiredFieldError(self, field)
        super(ModelCore, self).save(force_insert, force_update, using)

    def save_with_revision(self, user, force_insert=False, force_update=False, using=None):
        "Save a media object and add a revision"
        self.save(force_insert, force_update, using)
        Revision.touch(self, user)    

    def get_revision(self):
        return Revision.objects.filter(element_type=self.element_type, element_id=self.id).order_by('-time')[0]

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
        top.setAttribute("id", str(self.pk))
        fields = self.to_dict()
        for name, value in fields.iteritems():
            element = doc.createElement(self.get_dom_field_name(name))
            if isinstance(value, EnhancedModel):
                element.setAttribute('key', str(value.pk))
            value = unicode(value)
            element.appendChild(doc.createTextNode(value))
            top.appendChild(element)
        return doc
    
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
    def field_label(cls, field_name):
        try:
            return cls._meta.get_field(field_name).verbose_name
        except FieldDoesNotExist:
            try:
                return getattr(cls, field_name).verbose_name
            except AttributeError:
                return field_name

    class Meta:
        abstract = True

class MediaResource(ModelCore):
    "Base class of all media objects"

    class Meta:
        abstract = True

class MetaCore:
    app_label = 'telemeta'

class MediaCollection(MediaResource):
    "Describe a collection of items"
    element_type = 'collection'
    PUBLIC_ACCESS_CHOICES = (('none', 'none'), ('metadata', 'metadata'), ('metadata', 'full'))

    published_code_regex   = 'CNRSMH_E_[0-9]{4}(?:_[0-9]{3}){2}'
    unpublished_code_regex = 'CNRSMH_I_[0-9]{4}_[0-9]{3}'
    code_regex             = '(?:%s|%s)' % (published_code_regex, unpublished_code_regex)

    reference             = CharField(_('reference'), unique=True, null=True)
    physical_format       = WeakForeignKey('PhysicalFormat', related_name="collections", 
                                           verbose_name=_('archive format'))
    old_code              = CharField(_('old code'), unique=True, null=True)
    code                  = CharField(_('code'), unique=True, required=True)
    title                 = CharField(_('title'), required=True)
    alt_title             = CharField(_('original title / translation'))
    physical_items_num    = IntegerField(_('number of components (medium / piece)'))
    publishing_status     = WeakForeignKey('PublishingStatus', related_name="collections", 
                                           verbose_name=_('secondary edition'))
    creator               = CharField(_('depositor / contributor'))
    booklet_author        = CharField(_('author of published notice'))
    booklet_description   = TextField(_('related documentation'))
    collector             = CharField(_('collector'))
    collector_is_creator  = BooleanField(_('collector identical to depositor'))
    publisher             = WeakForeignKey('Publisher', related_name="collections", 
                                           verbose_name=_('publisher / status'))     
    is_published          = BooleanField(_('published'))
    year_published        = IntegerField(_('year published'))
    publisher_collection  = WeakForeignKey('PublisherCollection', related_name="collections", 
                                            verbose_name=_('publisher collection'))
    publisher_serial      = CharField(_('publisher serial number'))
    external_references   = TextField(_('bibliographic references'))
    acquisition_mode      = WeakForeignKey('AcquisitionMode', related_name="collections", 
                                            verbose_name=_('mode of acquisition'))
    comment               = TextField(_('comment'))
    metadata_author       = WeakForeignKey('MetadataAuthor', related_name="collections", 
                                           verbose_name=_('record author'))
    metadata_writer       = WeakForeignKey('MetadataWriter', related_name="collections", 
                                           verbose_name=_('record writer'))
    legal_rights          = WeakForeignKey('LegalRight', related_name="collections", 
                                           verbose_name=_('legal rights'))
    alt_ids               = CharField(_('copies'))
    recorded_from_year    = IntegerField(_('recording year (from)'))
    recorded_to_year      = IntegerField(_('recording year (until)'))
    recording_context     = WeakForeignKey('RecordingContext', related_name="collections", 
                                           verbose_name=_('recording context'))
    approx_duration       = DurationField(_('approximative duration'))
    doctype_code          = IntegerField(_('document type'))
    travail               = CharField(_('archiver notes'))
    state                 = TextField(_('status'))
    cnrs_contributor      = CharField(_('CNRS depositor'))
    items_done            = CharField(_('items finished'))
    a_informer_07_03      = CharField(_('a_informer_07_03'))
    ad_conversion         = WeakForeignKey('AdConversion', related_name='collections', 
                                           verbose_name=_('A/D conversion'))
    public_access         = CharField(_('public access'), choices=PUBLIC_ACCESS_CHOICES, 
                                      max_length=16, default="metadata")

    objects               = query.MediaCollectionManager()

    def __unicode__(self):
        return self.code

    @property
    def public_id(self):
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

    def countries(self):
        "Return the countries of the items"
        countries = []
        for item in self.items.filter(location__isnull=False):
            for country in item.location.countries():
                if not country in countries:
                    countries.append(country)
            
        countries.sort(self.__name_cmp)                

        return countries
    countries.verbose_name = _("states / nations")

    def ethnic_groups(self):
        "Return the ethnic groups of the items"
        groups = []
        items = self.items.all()
        for item in items:
            if item.ethnic_group and not item.ethnic_group in groups:
                groups.append(item.ethnic_group)

        groups.sort(self.__name_cmp)                

        return groups
    ethnic_groups.verbose_name = _('populations / social groups')

    def computed_duration(self):
        duration = Duration()
        for item in self.items.all():
            duration += item.computed_duration()

        return duration
    computed_duration.verbose_name = _('computed duration')        

    def is_valid_code(self, code):
        "Check if the collection code is well formed"
        if self.is_published:
            regex = '^' + self.published_code_regex + '$'
        else:
            regex = '^' + self.unpublished_code_regex + '$'
           
        if re.match(regex, code):
            return True

        return False

    def save(self, force_insert=False, force_update=False, using=None):
        if not self.code:
            raise RequiredFieldError(self, self._meta.get_field('code'))
        if not self.is_valid_code(self.code):
            raise MediaInvalidCodeError("%s is not a valid code for this collection" % self.code)
        super(MediaCollection, self).save(force_insert, force_update, using)

    class Meta(MetaCore):
        db_table = 'media_collections'

class MediaItem(MediaResource):
    "Describe an item"
    element_type = 'item'
    PUBLIC_ACCESS_CHOICES = (('none', 'none'), ('metadata', 'metadata'), ('full', 'full'))

    published_code_regex    = MediaCollection.published_code_regex + '(?:_[0-9]{2}){1,2}'
    unpublished_code_regex  = MediaCollection.unpublished_code_regex + '_[0-9]{2,3}(?:_[0-9]{2}){0,2}'
    code_regex              = '(?:%s|%s)' % (published_code_regex, unpublished_code_regex)

    collection            = ForeignKey('MediaCollection', related_name="items", 
                                       verbose_name=_('collection'))
    track                 = CharField(_('item number'))
    old_code              = CharField(_('old code'), unique=True, null=True)
    code                  = CharField(_('code'), unique=True, null=True)
    approx_duration       = DurationField(_('approximative duration'))
    recorded_from_date    = DateField(_('recording date (from)'))
    recorded_to_date      = DateField(_('recording date (until)'))
    location              = WeakForeignKey('Location', verbose_name=_('location'))
    location_comment      = CharField(_('location comment'))
    ethnic_group          = WeakForeignKey('EthnicGroup', related_name="items", 
                                           verbose_name=_('population / social group'))
    title                 = CharField(_('title'), required=True)
    alt_title             = CharField(_('original title / translation'))
    author                = CharField(_('author'))
    vernacular_style      = WeakForeignKey('VernacularStyle', related_name="items", 
                                           verbose_name=_('vernacular name'))
    context_comment       = TextField(_('comments'))
    external_references   = TextField(_('published reference'))
    moda_execut           = CharField(_('moda_execut'))
    copied_from_item      = WeakForeignKey('self', related_name="copies", verbose_name=_('copy of'))
    collector             = CharField(_('recorded by'))
    cultural_area         = CharField(_('cultural area'))
    generic_style         = WeakForeignKey('GenericStyle', related_name="items", 
                                           verbose_name=_('generic name'))
    collector_selection   = CharField(_('collector selection'))
    creator_reference     = CharField(_('reference'))
    comment               = TextField(_('comment'))
    file                  = FileField(_('file'), upload_to='items/%Y/%m/%d', db_column="filename")
    public_access         = CharField(_('public access'), choices=PUBLIC_ACCESS_CHOICES, max_length=16, default="metadata")

    objects               = query.MediaItemManager()

    def keywords(self):
        return ContextKeyword.objects.filter(item_relations__item = self)
    keywords.verbose_name = _('keywords')

    @property
    def public_id(self):
        if self.code:
            return self.code
        return self.id

    class Meta(MetaCore):
        db_table = 'media_items'

    def is_valid_code(self, code):
        "Check if the item code is well formed"
        if not re.match('^' + self.collection.code, self.code):
            return false

        if self.collection.is_published:
            regex = '^' + self.published_code_regex + '$'
        else:
            regex = '^' + self.unpublished_code_regex + '$'

        if re.match(regex, code):
            return True

        return False

    def save(self, force_insert=False, force_update=False, using=None):
        if not self.code:
            raise RequiredFieldError(self, self._meta.get_field('code'))
        if not self.is_valid_code(self.code):
            raise MediaInvalidCodeError("%s is not a valid item code for collection %s" 
                                        % (self.code, self.collection.code))
        super(MediaItem, self).save(force_insert, force_update, using)

    def computed_duration(self):
        "Tell the length in seconds of this item media data"
        # FIXME: use TimeSide?
        seconds = 0
        if self.file:
            import wave
            media = wave.open(self.file.path, "rb")
            seconds = media.getnframes() / media.getframerate()
            media.close()

        return Duration(seconds=seconds)

    computed_duration.verbose_name = _('computed duration')        

    def __unicode__(self):
        if self.code:
            return self.code
        return self.old_code

class MediaPart(MediaResource):
    "Describe an item part"
    element_type = 'part'
    item  = ForeignKey('MediaItem', related_name="parts", verbose_name=_('item'))
    title = CharField(_('title'), required=True)
    start = FloatField(_('start'), required=True)
    end   = FloatField(_('end'), required=True)
    
    class Meta(MetaCore):
        db_table = 'media_parts'

    def __unicode__(self):
        return self.title

class Enumeration(ModelCore):
    "Abstract enumerations base class"
    value = CharField(_('value'), required=True, unique=True)
    
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
    name    = CharField(_('name'), required=True)

    class Meta(MetaCore):
        db_table = 'instruments'

    def __unicode__(self):
        return self.name

class InstrumentAlias(ModelCore):
    "Instrument other name"
    name = CharField(_('name'), required=True)

    class Meta(MetaCore):
        db_table = 'instrument_aliases'

    def __unicode__(self):
        return self.name

class InstrumentRelation(ModelCore):
    "Instrument family"
    instrument        = ForeignKey('Instrument', related_name="parent_relation", 
                                   verbose_name=_('instrument'))
    parent_instrument = ForeignKey('Instrument', related_name="child_relation", 
                                   verbose_name=_('parent instrument'))

    class Meta(MetaCore):
        db_table = 'instrument_relations'
        unique_together = (('instrument', 'parent_instrument'),)

class InstrumentAliasRelation(ModelCore):
    "Instrument family other name"
    alias      = ForeignKey('InstrumentAlias', related_name="other_name", 
                            verbose_name=_('alias'))
    instrument = ForeignKey('InstrumentAlias', related_name="relation", 
                            verbose_name=_('instrument'))

    class Meta(MetaCore):
        db_table = 'instrument_alias_relations'
        unique_together = (('alias', 'instrument'),)

class MediaItemPerformance(ModelCore):
    "Item performance"
    media_item      = ForeignKey('MediaItem', related_name="performances", 
                                 verbose_name=_('item'))
    instrument      = WeakForeignKey('Instrument', related_name="performances", 
                                     verbose_name=_('scientific instrument'))
    alias           = WeakForeignKey('InstrumentAlias', related_name="performances", 
                                     verbose_name=_('vernacular instrument'))
    instruments_num = CharField(_('number'))
    musicians       = CharField(_('interprets'))

    class Meta(MetaCore):
        db_table = 'media_item_performances'

class User(ModelCore):
    "Telemeta user"
    LEVEL_CHOICES = (('user', 'user'), ('maintainer', 'maintainer'), ('admin', 'admin'))    

    username   = CharField(_('username'), primary_key=True, max_length=64, required=True)
    level      = CharField(_('level'), choices=LEVEL_CHOICES, max_length=32, required=True)
    first_name = CharField(_('first name'))
    last_name  = CharField(_('last name'))
    phone      = CharField(_('phone'))
    email      = CharField(_('email'))

    class Meta(MetaCore):
        db_table = 'users'

    def __unicode__(self):
        return self.username

class Playlist(ModelCore):
    "Item or collection playlist"
    owner_username = ForeignKey('User', related_name="playlists", db_column="owner_username") 
    name           = CharField(_('name'), required=True)

    class Meta(MetaCore):
        db_table = 'playlists'

    def __unicode__(self):
        return self.name

class PlaylistResource(ModelCore):
    "Playlist components"
    RESOURCE_TYPE_CHOICES = (('item', 'item'), ('collection', 'collection'))

    playlist              = ForeignKey('Playlist', related_name="resources", verbose_name=_('playlist'))
    resource_type         = CharField(_('resource type'), choices=RESOURCE_TYPE_CHOICES, required=True)
    resource              = IntegerField(_('resource'), required=True)

    class Meta(MetaCore):
        db_table = 'playlist_resources'

class Location(ModelCore):
    "Locations"
    OTHER_TYPE  = 0
    CONTINENT   = 1
    COUNTRY     = 2
    TYPE_CHOICES     = ((COUNTRY, _('country')), (CONTINENT, _('continent')), (OTHER_TYPE, _('other')))

    name             = CharField(_('name'), unique=True, max_length=150, required=True)
    type             = IntegerField(_('type'), choices=TYPE_CHOICES, required=True, db_index=True)
    complete_type    = ForeignKey('LocationType', related_name="locations", verbose_name=_('complete type'))
    current_location = WeakForeignKey('self', related_name="past_names", 
                                      verbose_name=_('current location')) 
    is_authoritative = BooleanField(_('authoritative'))

    objects = query.LocationManager()

    def items(self):
        return MediaItem.objects.by_location(self)

    def collections(self):
        return MediaCollection.objects.by_location(self)

    def ancestors(self):
        return Location.objects.filter(descendant_relations__location=self)

    def descendants(self):
        return Location.objects.filter(ancestor_relations__ancestor_location=self)

    def countries(self):
        if self.type == self.COUNTRY:
            return Location.objects.filter(pk=self.id)
        return self.ancestors().filter(type=self.COUNTRY)

    class Meta(MetaCore):
        db_table = 'locations'

    def __unicode__(self):
        return self.name

    def flatname(self):
        if self.type != self.COUNTRY and self.type != self.CONTINENT:
            raise Exceptions("Flat names are only supported for countries and continents")

        map = Location.objects.flatname_map()
        for flatname in map:
            if self.id == map[flatname]:
                return flatname

        return None                    

    def sequences(self):
        sequence = []
        location = self
        while location:
            sequence.append(location)
            location = location.parent()
        return sequence

    def fullnames(self):
        
        return u', '.join([unicode(l) for l in self.sequence()])

class LocationType(ModelCore):
    "Location types"
    code = CharField(_('identifier'), max_length=64, unique=True, required=True)
    name = CharField(_('name'), max_length=150, required=True)

    class Meta(MetaCore):
        db_table = 'location_types'

class LocationAlias(ModelCore):
    "Location aliases"
    location         = ForeignKey('Location', related_name="aliases", verbose_name=_('location'))
    alias            = CharField(_('alias'), max_length=150, required=True)
    is_authoritative = BooleanField(_('authoritative'))

    def __unicode__(self):
        return self.alias

    class Meta(MetaCore):
        db_table = 'location_aliases'
        unique_together = (('location', 'alias'),)
    
class LocationRelation(ModelCore):
    "Location relations"
    location             = ForeignKey('Location', related_name="ancestor_relations", verbose_name=_('location'))
    ancestor_location      = ForeignKey('Location', related_name="descendant_relations",  verbose_name=_('ancestor location'))
    is_direct            = BooleanField(db_index=True)

    class Meta(MetaCore):
        db_table = 'location_relations'
        unique_together = ('location', 'ancestor_location')
    
class ContextKeyword(Enumeration):
    "Keyword"

    class Meta(MetaCore):
        db_table = 'context_keywords'

class MediaItemKeyword(ModelCore):
    "Item keyword"
    item    = ForeignKey('MediaItem', verbose_name=_('item'), related_name="keyword_relations")
    keyword = ForeignKey('ContextKeyword', verbose_name=_('keyword'), related_name="item_relations")

    class Meta(MetaCore):
        db_table = 'media_item_keywords'
        unique_together = (('item', 'keyword'),)

class Publisher(Enumeration): 
    "Collection publisher"

    class Meta(MetaCore):
        db_table = 'publishers'

class PublisherCollection(ModelCore):
    "Collection which belongs to publisher"
    publisher = ForeignKey('Publisher', related_name="publisher_collections", verbose_name=_('publisher'))
    value     = CharField(_('value'), required=True)

    def __unicode__(self):
        return self.value

    class Meta(MetaCore):
        db_table = 'publisher_collections'

class Revision(ModelCore):
    "Revision made by user"
    ELEMENT_TYPE_CHOICES = (('collection', 'collection'), ('item', 'item'), ('part', 'part'))
    CHANGE_TYPE_CHOICES  = (('import', 'import'), ('create', 'create'), ('update', 'update'), ('delete','delete'))

    element_type         = CharField(_('element type'), choices=ELEMENT_TYPE_CHOICES, max_length=16, required=True)
    element_id           = IntegerField(_('element identifier'), required=True)
    change_type          = CharField(_('modification type'), choices=CHANGE_TYPE_CHOICES, max_length=16, required=True)
    time                 = DateTimeField(_('time'), auto_now_add=True)
    user                 = ForeignKey('User', db_column='username', related_name="revisions", verbose_name=_('user'))
    
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
    name = CharField(_('name'), required=True)

    class Meta(MetaCore):
        db_table = 'ethnic_groups'

    def __unicode__(self):
        return self.name

class EthnicGroupAlias(ModelCore):
    "Item ethnic group other name" 
    ethnic_group = ForeignKey('EthnicGroup', related_name="aliases", verbose_name=_('population / social group'))
    name         = CharField(_('name'), required=True)

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

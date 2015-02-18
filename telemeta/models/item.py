# -*- coding: utf-8 -*-
# Copyright (C) 2010 Samalyse SARL
# Copyright (C) 2010-2014 Parisson SARL

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
#          Guillaume Pellerin <yomguy@parisson.com>

from __future__ import division
from django.utils.translation import ugettext_lazy as _
from telemeta.models.core import *
from telemeta.models.resource import *
from telemeta.models.query import *
from telemeta.models.identifier import *
from telemeta.models.resource import *
from telemeta.models.enum import *


item_published_code_regex = getattr(settings, 'ITEM_PUBLISHED_CODE_REGEX', '[A-Za-z0-9._-]*')
item_unpublished_code_regex = getattr(settings, 'ITEM_UNPUBLISHED_CODE_REGEX', '[A-Za-z0-9._-]*')

# CREM
# item_published_code_regex    = collection_published_code_regex + '(?:_[0-9]{2,3}){1,2}'
# item_unpublished_code_regex  = collection_unpublished_code_regex + '_[0-9]{2,3}(?:_[0-9]{2,3}){0,2}'

item_code_regex = '(?:%s|%s)' % (item_published_code_regex, item_unpublished_code_regex)

ITEM_PUBLIC_ACCESS_CHOICES = (('none', _('none')), ('metadata', _('metadata')),
                         ('full', _('full')))

ITEM_TRANSODING_STATUS = ((0, _('broken')), (1, _('pending')), (2, _('processing')),
                         (3, _('done')), (5, _('ready')))


class MediaItem(MediaResource):
    "Describe an item"

    element_type = 'item'

    # Main Informations
    title                 = CharField(_('title'))
    alt_title             = CharField(_('original title / translation'))
    collector             = CharField(_('collector'), help_text=_('First name, Last name ; First name, Last name'))
    collection            = ForeignKey('MediaCollection', related_name="items", verbose_name=_('collection'))
    recorded_from_date    = DateField(_('recording date (from)'), help_text=_('YYYY-MM-DD'))
    recorded_to_date      = DateField(_('recording date (until)'), help_text=_('YYYY-MM-DD'))
    public_access         = CharField(_('access type'), choices=ITEM_PUBLIC_ACCESS_CHOICES, max_length=16, default="metadata")

    # Geographic and cultural informations
    location              = WeakForeignKey('Location', verbose_name=_('location'))
    location_comment      = CharField(_('location details'))
    cultural_area         = CharField(_('cultural area'))
    language              = CharField(_('language'))
    language_iso          = ForeignKey('Language', related_name="items", verbose_name=_('Language (ISO norm)'), blank=True, null=True, on_delete=models.SET_NULL)
    ethnic_group          = WeakForeignKey('EthnicGroup', related_name="items", verbose_name=_('population / social group'))
    context_comment       = TextField(_('Ethnographic context'))

    # Musical informations
    moda_execut           = CharField(_('implementing rules'))
    vernacular_style      = WeakForeignKey('VernacularStyle', related_name="items", verbose_name=_('vernacular style'))
    generic_style         = WeakForeignKey('GenericStyle', related_name="items", verbose_name=_('generic style'))
    author                = CharField(_('author / compositor'), help_text=_('First name, Last name ; First name, Last name'))

    # Legal mentions
    organization          = WeakForeignKey('Organization', verbose_name=_('organization'))
    depositor             = CharField(_('depositor'))
    rights                = WeakForeignKey('Rights', verbose_name=_('rights'))

    # Archiving data
    code                  = CharField(_('code'), unique=True, blank=True, required=True, help_text=_('CollectionCode_ItemCode'))
    old_code              = CharField(_('original code'), unique=False, blank=True)
    track                 = CharField(_('item number'))
    collector_selection   = CharField(_('collector selection'))
    collector_from_collection = BooleanField(_('collector as in collection'))
    creator_reference     = CharField(_('creator reference'))
    external_references   = TextField(_('published references'))
    auto_period_access    = BooleanField(_('automatic access after a rolling period'), default=True)
    comment               = TextField(_('remarks'))

    # Technical data
    media_type            = WeakForeignKey('MediaType', related_name="items", verbose_name=_('media type'))
    approx_duration       = DurationField(_('approximative duration'), blank=True, help_text=_('hh:mm:ss'))
    mimetype              = CharField(_('mime type'), max_length=255, blank=True)
    file                  = FileField(_('file'), upload_to='items/%Y/%m/%d', db_column="filename", max_length=1024)
    url                   = URLField(_('URL'), max_length=512, blank=True)

    # LAM
    recordist             = CharField(_('recordist'))
    digitalist            = CharField(_('digitalist'))
    digitization_date     = DateField(_('digitization date'))
    publishing_date       = DateField(_('publishing date'))
    scientist             = CharField(_('scientist'), help_text=_('First name, Last name ; First name, Last name'))
    topic                 = WeakForeignKey('Topic', verbose_name=_('topic'))
    summary               = TextField(_('summary'))
    contributor           = CharField(_('contributor'))

    # Manager
    objects               = MediaItemManager()

    exclude = ['copied_from_item', 'mimetype', 'url',
                    'organization', 'depositor', 'rights',
                    'recordist', 'digitalist', 'digitization_date',
                    'publishing_date', 'scientist', 'topic',
                    'summary', 'contributor', ]

    def keywords(self):
        return ContextKeyword.objects.filter(item_relations__item = self)
    keywords.verbose_name = _('keywords')

    @property
    def public_id(self):
        if self.code:
            return self.code
        return str(self.id)

    @property
    def mime_type(self):
        if not self.mimetype:
            if self.file:
                if os.path.exists(self.file.path):
                    self.mimetype = mimetypes.guess_type(self.file.path)[0]
                    self.save()
                    return self.mimetype
                else:
                    return 'none'
            else:
                return 'none'
        else:
            return _('none')


    class Meta(MetaCore):
        db_table = 'media_items'
        permissions = (("can_play_all_items", "Can play all media items"),
                       ("can_download_all_items", "Can download all media items"), )
        verbose_name = _('item')

    def is_valid_code(self, code):
        "Check if the item code is well formed"
        if not re.match('^' + self.collection.code, self.code):
            return False
        if self.collection.is_published:
            regex = '^' + item_published_code_regex + '$'
        else:
            regex = '^' + item_unpublished_code_regex + '$'
        if re.match(regex, code):
            return True
        return False

    def clean(self):
        if strict_code:
            if self.code and not self.is_valid_code(self.code):
                raise ValidationError("%s is not a valid item code for collection %s"
                                            % (self.code, self.collection.code))

    def save(self, force_insert=False, force_update=False):
        super(MediaItem, self).save(force_insert, force_update)

    def computed_duration(self):
        "Tell the length in seconds of this item media data"
        return self.approx_duration

    computed_duration.verbose_name = _('computed duration')

    def __unicode__(self):
        if self.title and not re.match('^ *N *$', self.title):
            title = self.title
        else:
            title = unicode(self.collection.title)
        if self.track:
            title += ' ' + self.track
        return title

    def get_source(self):
        source = None
        if self.file and os.path.exists(self.file.path):
            source = self.file.path
        elif self.url:
            source = self.url
        return source

    @property
    def instruments(self):
        "Return the instruments of the item"
        instruments = []
        performances = MediaItemPerformance.objects.filter(media_item=self)
        for performance in performances:
            instrument = performance.instrument
            alias = performance.alias
            if not instrument in instruments:
                instruments.append(instrument)
            if not alias in instruments:
                instruments.append(alias)

        instruments.sort(self.__name_cmp)
        return instruments

        instruments.verbose_name = _("instruments")

    def size(self):
        if self.file and os.path.exists(self.file.path):
            return self.file.size
        else:
            return 0
    size.verbose_name = _('item size')

    def get_url(self):
        return get_full_url(reverse('telemeta-item-detail', kwargs={'public_id':self.pk}))

    def to_dict_with_more(self):
        # metadata = model_to_dict(self, fields=[], exclude=self.exclude)
        metadata = self.to_dict()
        for key in self.exclude:
            if key in metadata.keys():
                del metadata[key]

        metadata['url'] = self.get_url()
        metadata['last_modification_date'] = unicode(self.get_revision().time)
        metadata['collection'] = self.collection.get_url()

        keywords = []
        for keyword in self.keywords():
            keywords.append(keyword.value)
        metadata['keywords'] = ';'.join(keywords)

        i = 0
        for media in self.related.all():
            if media.title:
                tag = 'related_media_title' + '_' + str(i)
                metadata[tag] = media.title
            else:
                metadata[tag] = ''
            if media.url:
                tag = 'related_media_url' + '_' + str(i)
                metadata[tag] = media.url
            elif media.url:
                metadata[tag] = get_full_url(reverse('telemeta-collection-related',
                                            kwargs={'public_id': self.public_id, 'media_id': media.id}))
            i += 1


        instruments = []
        instrument_vernacular_names = []
        performers = []

        for performance in self.performances.all():
            if performance.instrument:
                instruments.append(performance.instrument.name)
            if performance.alias:
                instrument_vernacular_names.append(performance.alias.name)
            if performance.musicians:
                performers.append(performance.musicians.replace(' et ', ';'))

        metadata['instruments'] = ';'.join(instruments)
        metadata['instrument_vernacular_names'] = ';'.join(instrument_vernacular_names)
        metadata['performers'] = ';'.join(performers)

        i = 0
        for indentifier in self.identifiers.all():
            metadata['identifier' + '_' + str(i)] = identifier.identifier
            metadata['identifier_type' + '_' + str(i)] = identifier.type
            metadata['identifier_date_last' + '_' + str(i)] = unicode(identifier.date_last)
            metadata['identifier_notes' + '_' + str(i)] = identifier.notes
            i += 1

        analyzers = ['channels', 'samplerate', 'duration', 'resolution', 'mime_type']
        for analyzer_id in analyzers:
            analysis = MediaItemAnalysis.objects.filter(item=self, analyzer_id=analyzer_id)
            if analysis:
                metadata[analyzer_id] = analysis[0].value

        metadata['file_size'] = unicode(self.size())
        metadata['thumbnail'] = get_full_url(reverse('telemeta-item-visualize',
                                            kwargs={'public_id': self.public_id,
                                                    'grapher_id': 'waveform_centroid',
                                                    'width': 346,
                                                    'height': 130}))

        # One ID only
        identifiers = self.identifiers.all()
        if identifiers:
            identifier = identifiers[0]
            metadata['identifier_id'] = identifier.identifier
            metadata['identifier_type'] = identifier.type
            metadata['identifier_date'] = unicode(identifier.date_last)
            metadata['identifier_note'] = identifier.notes

        return metadata


class MediaItemRelated(MediaRelated):
    "Item related media"

    item = ForeignKey('MediaItem', related_name="related", verbose_name=_('item'))

    def save(self, force_insert=False, force_update=False, using=False):
        super(MediaItemRelated, self).save(force_insert, force_update)

    def parse_markers(self, **kwargs):
        # Parse KDEnLive session
        if self.file:
            if self.is_kdenlive_session():
                session = KDEnLiveSession(self.file.path)
                markers = session.markers(**kwargs)
                for marker in markers:
                    m = MediaItemMarker(item=self.item)
                    m.public_id = get_random_hash()
                    m.time = float(marker['time'])
                    m.title = marker['comment']
                    m.save()
                return markers

    class Meta(MetaCore):
        db_table = 'media_item_related'
        verbose_name = _('item related media')
        verbose_name_plural = _('item related media')


class MediaItemKeyword(ModelCore):
    "Item keyword"
    item    = ForeignKey('MediaItem', verbose_name=_('item'), related_name="keyword_relations")
    keyword = ForeignKey('ContextKeyword', verbose_name=_('keyword'), related_name="item_relations")

    class Meta(MetaCore):
        db_table = 'media_item_keywords'
        unique_together = (('item', 'keyword'),)


class MediaItemPerformance(ModelCore):
    "Item performance"
    media_item      = ForeignKey('MediaItem', related_name="performances", verbose_name=_('item'))
    instrument      = WeakForeignKey('Instrument', related_name="performances", verbose_name=_('composition'))
    alias           = WeakForeignKey('InstrumentAlias', related_name="performances", verbose_name=_('vernacular name'))
    instruments_num = CharField(_('number'))
    musicians       = CharField(_('interprets'))

    class Meta(MetaCore):
        db_table = 'media_item_performances'


class MediaItemAnalysis(ModelCore):
    "Item analysis result computed by TimeSide"

    element_type = 'analysis'
    item  = ForeignKey('MediaItem', related_name="analysis", verbose_name=_('item'))
    analyzer_id = CharField(_('id'), required=True)
    name = CharField(_('name'))
    value = CharField(_('value'))
    unit = CharField(_('unit'))

    class Meta(MetaCore):
        db_table = 'media_analysis'
        ordering = ['name']

    def to_dict(self):
        if self.analyzer_id == 'duration':
            if '.' in self.value:
                value = self.value.split('.')
                self.value = '.'.join([value[0], value[1][:2]])
        return {'id': self.analyzer_id, 'name': self.name, 'value': self.value, 'unit': self.unit}



class MediaItemMarker(MediaResource):
    "2D marker object : text value vs. time (in seconds)"

    element_type = 'marker'

    item            = ForeignKey('MediaItem', related_name="markers", verbose_name=_('item'))
    public_id       = CharField(_('public_id'), required=True)
    time            = FloatField(_('time (s)'))
    title           = CharField(_('title'))
    date            = DateTimeField(_('date'), auto_now=True)
    description     = TextField(_('description'))
    author          = ForeignKey(User, related_name="markers", verbose_name=_('author'),
                                 blank=True, null=True)

    class Meta(MetaCore):
        db_table = 'media_markers'
        ordering = ['time']

    def __unicode__(self):
        if self.title:
            return self.title
        else:
            return self.public_id


class MediaItemTranscoded(MediaResource):
    "Item file transcoded"

    element_type = 'transcoded item'

    item            = models.ForeignKey('MediaItem', related_name="transcoded", verbose_name=_('item'))
    mimetype        = models.CharField(_('mime_type'), max_length=255, blank=True)
    date_added      = DateTimeField(_('date'), auto_now_add=True)
    status          = models.IntegerField(_('status'), choices=ITEM_TRANSODING_STATUS, default=1)
    file            = models.FileField(_('file'), upload_to='items/%Y/%m/%d', max_length=1024, blank=True)

    @property
    def mime_type(self):
        if not self.mimetype:
            if self.file:
                if os.path.exists(self.file.path):
                    self.mimetype = mimetypes.guess_type(self.file.path)[0]
                    self.save()
                    return self.mimetype
                else:
                    return 'none'
            else:
                return 'none'
        else:
            return self.mimetype

    def __unicode__(self):
        if self.item.title:
            return self.item.title + ' - ' + self.mime_type
        else:
            return self.item.public_id + ' - ' + self.mime_type

    class Meta(MetaCore):
        db_table = app_name + '_media_transcoded'


class MediaItemTranscodingFlag(ModelCore):
    "Item flag to know if the MediaItem has been transcoded to a given format"

    item            = ForeignKey('MediaItem', related_name="transcoding", verbose_name=_('item'))
    mime_type       = CharField(_('mime_type'), required=True)
    date            = DateTimeField(_('date'), auto_now=True)
    value           = BooleanField(_('transcoded'))

    class Meta(MetaCore):
        db_table = 'media_transcoding'


class MediaItemIdentifier(Identifier):
    """Item identifier"""

    item = ForeignKey(MediaItem, related_name="identifiers", verbose_name=_('item'))

    class Meta(MetaCore):
        db_table = 'media_item_identifier'
        verbose_name = _('item identifier')
        verbose_name_plural = _('item identifiers')
        unique_together = ('identifier', 'item')


class MediaPart(MediaResource):
    "Describe an item part"
    element_type = 'part'
    item  = ForeignKey('MediaItem', related_name="parts", verbose_name=_('item'))
    title = CharField(_('title'), required=True)
    start = FloatField(_('start'), required=True)
    end   = FloatField(_('end'), required=True)

    class Meta(MetaCore):
        db_table = 'media_parts'
        verbose_name = _('item part')

    def __unicode__(self):
        return self.title

# -*- coding: utf-8 -*-
# Copyright (C) 2010 Samalyse SARL
# Copyright (C) 2010-2014 Parisson SARL

# This file is part of Telemeta.

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
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

    exclude = ['copied_from_item', 'mimetype',
                    'organization', 'depositor', 'rights',
                    'recordist', 'digitalist', 'digitization_date',
                    'publishing_date', 'scientist', 'topic',
                    'summary', 'contributor', ]

    restricted = ['copied_from_item', 'mimetype',
                    'organization', 'depositor', 'rights',
                    'recordist', 'digitalist', 'digitization_date',
                    'publishing_date', 'scientist', 'topic',
                    'summary', 'contributor', 'public_access']

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
                       ("can_download_all_items", "Can download all media items"),
                       ("can_run_analysis", "Can run analysis"),)
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

    def save(self, force_insert=False, force_update=False, *args, **kwargs):
        super(MediaItem, self).save(force_insert, force_update, *args, **kwargs)

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
        source_type = None
        if self.file and os.path.exists(self.file.path):
            source = self.file.path
            source_type = 'file'
        elif self.url:
            source = self.url
            source_type = 'url'
        return source, source_type

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
        #no reference for __name_cmp anywhere
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
        revision = self.get_revision()
        if revision:
            time = unicode(revision.time)
        else:
            time = ''
        metadata['last_modification_date'] = time
        metadata['collection'] = self.collection.get_url()

        keywords = []
        for keyword in self.keywords():
            keywords.append(keyword.value)
        metadata['keywords'] = ';'.join(keywords)

        related_media_urls = []
        for media in self.related.all():
            if media.url:
                related_media_urls.append(media.url)
            else:
                try:
                    url = get_full_url(reverse('telemeta-item-related',
                                                kwargs={'public_id': self.public_id, 'media_id': media.id}))
                except:
                    url = ''
                related_media_urls.append(url)
        metadata['related_media_urls'] = ';'.join(related_media_urls)

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

        analyzers = ['channels', 'samplerate', 'duration', 'resolution', 'mime_type']
        for analyzer_id in analyzers:
            analysis = MediaItemAnalysis.objects.filter(item=self, analyzer_id=analyzer_id)
            if analysis:
                if analyzer_id == 'duration':
                    value = ':'.join([str('%.2d' % int(float(t))) for t in analysis[0].value.split(':')])
                else:
                    value = analysis[0].value
                metadata[analyzer_id] = value
            elif analyzer_id == 'duration':
                metadata[analyzer_id] = self.approx_duration
            else:
                metadata[analyzer_id] = ''

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
        else:
            metadata['identifier_id'] = ''
            metadata['identifier_type'] = ''
            metadata['identifier_date'] = ''
            metadata['identifier_note'] = ''

        # Collection
        metadata['recording_context'] = self.collection.recording_context
        metadata['description_collection'] = self.collection.description
        metadata['status'] = self.collection.status
        metadata['original_format'] = self.collection.original_format
        metadata['physical_format'] = self.collection.physical_format
        metadata['year_published'] = self.collection.year_published
        metadata['publisher'] = self.collection.publisher
        metadata['publisher_collection'] = self.collection.publisher_collection
        metadata['reference_collection'] = self.collection.reference

        return metadata

    def to_row(self, tags):
        row = []
        _dict = self.to_dict_with_more()
        for tag in tags:
            if tag in _dict.keys():
                row.append(_dict[tag])
            else:
                row.append('')
        return row

class MediaItemRelated(MediaRelated):
    "Item related media"

    item = ForeignKey('MediaItem', related_name="related", verbose_name=_('item'))

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

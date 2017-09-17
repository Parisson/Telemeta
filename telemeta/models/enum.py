# -*- coding: utf-8 -*-
# Copyright (C) 2007-2010 Samalyse SARL

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

from telemeta.models.core import *
from django.utils.translation import ugettext_lazy as _


class Enumeration(ModelCore):
    "Abstract enumerations base class"

    value = CharField(_('value'), required=True, unique=True)
    notes = TextField(_('notes'))

    def __unicode__(self):
        return self.value

    class Meta(MetaCore):
        abstract = True


class MetaEnumeration(MetaCore):
    ordering = ['value']


class EnumerationProperty(ModelCore):

    enumeration_name = models.CharField(_('enumeration name'), max_length=255)
    is_hidden = BooleanField(_('is hidden'), default=False)
    is_admin = BooleanField(_('is admin'), default=True)

    class Meta(MetaCore):
        verbose_name = _("enumeration property")
        verbose_name_plural = _("enumeration properties")

    def __unicode__(self):
        return self.enumeration_name


class PhysicalFormat(Enumeration):
    "Collection physical format"

    class Meta(MetaEnumeration):
        db_table = 'physical_formats'
        verbose_name = _("archive format")


class PublishingStatus(Enumeration):
    "Collection publishing status"

    class Meta(MetaEnumeration):
        db_table = 'publishing_status'
        verbose_name = _("secondary edition")


class AcquisitionMode(Enumeration):
    "Mode of acquisition of the collection"

    class Meta(MetaEnumeration):
        db_table = 'acquisition_modes'
        verbose_name = _("mode of acquisition")


class MetadataAuthor(Enumeration):
    "Collection metadata author"

    class Meta(MetaEnumeration):
        db_table = 'metadata_authors'
        verbose_name = _("record author")


class MetadataWriter(Enumeration):
    "Collection metadata writer"

    class Meta(MetaEnumeration):
        db_table = 'metadata_writers'
        verbose_name = _("record writer")


class LegalRight(Enumeration):
    "Collection legal rights"

    class Meta(MetaEnumeration):
        db_table = 'legal_rights'
        verbose_name = _("legal rights")


class RecordingContext(Enumeration):
    "Collection recording context"

    class Meta(MetaEnumeration):
        db_table = 'recording_contexts'
        verbose_name = _("recording context")

class AdConversion(Enumeration):
    "Collection digital to analog conversion status"

    class Meta(MetaEnumeration):
        db_table = 'ad_conversions'
        verbose_name = _("A/D conversion")

class VernacularStyle(Enumeration):
    "Item vernacular style"

    class Meta(MetaEnumeration):
        db_table = 'vernacular_styles'
        verbose_name = _("vernacular style")

class GenericStyle(Enumeration):
    "Item generic style"

    class Meta(MetaEnumeration):
        db_table = 'generic_styles'
        verbose_name = _("generic style")

class ContextKeyword(Enumeration):
    "Keyword"

    class Meta(MetaEnumeration):
        db_table = 'context_keywords'
        verbose_name = _("keyword")

class Publisher(Enumeration):
    "Collection publisher"

    class Meta(MetaEnumeration):
        db_table = 'publishers'
        verbose_name = _("publisher")


class PublisherCollection(ModelCore):
    "Collection which belongs to publisher"

    publisher = ForeignKey('Publisher', related_name="publisher_collections", verbose_name=_('publisher'))
    value     = CharField(_('value'), required=True)

    def __unicode__(self):
        return self.value

    class Meta(MetaCore):
        db_table = 'publisher_collections'
        ordering = ['value']


class EthnicGroup(Enumeration):
    "Item ethnic group"

    class Meta(MetaEnumeration):
        db_table = 'ethnic_groups'
        verbose_name = _('population / social group')


class EthnicGroupAlias(ModelCore):
    "Item ethnic group other name"

    ethnic_group = ForeignKey('EthnicGroup', related_name="aliases", verbose_name=_('population / social group'))
    value        = CharField(_('name'), required=True)

    class Meta(MetaCore):
        db_table = 'ethnic_group_aliases'
        unique_together = (('ethnic_group', 'value'),)
        ordering = ['ethnic_group__value']


# Tape formats
class TapeWheelDiameter(Enumeration):
    "Tape wheel diameter (cm)"

    class Meta(MetaEnumeration):
        db_table = 'tape_wheel_diameter'
        verbose_name = _("tape wheel diameter (cm)")

class TapeLength(Enumeration):
    "Tape length (cm)"

    class Meta(MetaEnumeration):
        db_table = 'tape_length'
        verbose_name = _("tape length (cm)")

class TapeWidth(Enumeration):
    "Tape width (inch)"

    class Meta(MetaEnumeration):
        db_table = 'tape_width'
        verbose_name = _("tape width (inch)")

class TapeSpeed(Enumeration):
    "Tape speed (cm/s)"

    class Meta(MetaEnumeration):
        db_table = 'tape_speed'
        verbose_name = _("tape speed (cm/s)")

class TapeVendor(Enumeration):
    "Tape vendor"

    class Meta(MetaEnumeration):
        db_table = 'tape_vendor'
        verbose_name = _("tape brand")


class NumberOfChannels(Enumeration):
    "Number of channels"

    class Meta(MetaEnumeration):
        db_table = 'original_channel_number'
        verbose_name = _("number of channels")


class Organization(Enumeration):
    "Organization"

    class Meta(MetaEnumeration):
        db_table = 'organization'
        verbose_name = _("organization")


class Rights(Enumeration):
    "Archive rights"

    class Meta(MetaEnumeration):
        db_table = 'rights'
        verbose_name = _("rights")


class Topic(Enumeration):
    "Topic, subject of the study, research, etc.."

    class Meta(MetaEnumeration):
        db_table = 'topic'
        verbose_name = _("topic")


class CopyType(Enumeration):
    "Type of the copy"

    class Meta(MetaEnumeration):
        db_table = 'copy_type'
        verbose_name = _("copy type")


class MediaType(Enumeration):
    "Type of the media"

    class Meta(MetaEnumeration):
        db_table = 'media_type'
        verbose_name = _("media type")


class OriginalFormat(Enumeration):
    "Original format"

    class Meta(MetaEnumeration):
        db_table = 'original_format'
        verbose_name = _("original format")


class Status(Enumeration):
    "Resource status"

    class Meta(MetaEnumeration):
        db_table = 'media_status'
        verbose_name = _("collection status")


class IdentifierType(Enumeration):
    "Identifier type"

    class Meta(MetaEnumeration):
        db_table = 'identifier_type'
        verbose_name = _("identifier type")

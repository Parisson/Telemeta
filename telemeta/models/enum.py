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

from telemeta.models.core import *
from django.utils.translation import ugettext_lazy as _

class Enumeration(ModelCore):
    "Abstract enumerations base class"
    value = CharField(_('value'), required=True, unique=True)
    
    def __unicode__(self):
        return self.value

    class Meta(MetaCore):
        abstract = True

class MetaEnumeration(MetaCore):
    ordering = ['value']

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
        verbose_name = _("publisher / status")

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



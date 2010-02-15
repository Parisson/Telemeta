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

class ContextKeyword(Enumeration):
    "Keyword"

    class Meta(MetaCore):
        db_table = 'context_keywords'

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

class EthnicGroup(ModelCore):
    "Item ethnic group"
    name = CharField(_('name'), required=True)

    class Meta(MetaCore):
        db_table = 'ethnic_groups'
        verbose_name = _('population / social group')

    def __unicode__(self):
        return self.name

class EthnicGroupAlias(ModelCore):
    "Item ethnic group other name" 
    ethnic_group = ForeignKey('EthnicGroup', related_name="aliases", verbose_name=_('population / social group'))
    name         = CharField(_('name'), required=True)

    class Meta(MetaCore):
        db_table = 'ethnic_group_aliases'



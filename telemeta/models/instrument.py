# -*- coding: utf-8 -*-
# Copyright (C) 2007-2010 Samalyse SARL
# Copyright (C) 2010-2011 Parisson SARL

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

from telemeta.models.core import *
from django.utils.translation import ugettext_lazy as _

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
        verbose_name_plural = _('instrument aliases')

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
    
    def __unicode__(self):
        sep = ' > '
        return self.parent_instrument.name + sep + self.instrument.name

class InstrumentAliasRelation(ModelCore):
    "Instrument family other name"
    alias      = ForeignKey('InstrumentAlias', related_name="other_name", 
                            verbose_name=_('alias'))
    instrument = ForeignKey('InstrumentAlias', related_name="relation", 
                            verbose_name=_('instrument'))

    def __unicode__(self):
        sep = ' : '
        return self.alias.name + sep + self.instrument.name
        
    class Meta(MetaCore):
        db_table = 'instrument_alias_relations'
        unique_together = (('alias', 'instrument'),)


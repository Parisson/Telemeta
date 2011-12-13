# -*- coding: utf-8 -*-
# Copyright (C) 2011-2012 Parisson SARL

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
# Authors:
#          Guillaume Pellerin <yomguy@parisson.com>

from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from telemeta.models.core import *

SCOPE_CHOICES = (('I', 'Individual'), ('M', 'Macrolanguage'), ('S', 'Special'))

TYPE_CHOICES = (('A', 'Ancient'), ('C', 'Constructed'), ('E', 'Extinct'),
                ('H', 'Historical'), ('L', 'Living'), ('S', 'Special'))

class Language(ModelCore):
    "ISO 639-3 normalized languages"

    identifier      = CharField(_('identifier'), max_length=3)
    part2B          = CharField(_('equivalent ISO 639-2 identifier (bibliographic)'), max_length=3)
    part2T          = CharField(_('equivalent ISO 639-2 identifier (terminologic)'), max_length=3)
    part1           = CharField(_('equivalent ISO 639-1 identifier'), max_length=1)
    scope           = CharField(_('scope'), choices=SCOPE_CHOICES, max_length=1)
    type            = CharField(_('type'), choices=TYPE_CHOICES, max_length=1)
    name            = CharField(_('name'))
    comment         = TextField(_('comment'))

    def __str__(self):
        return self.name.encode('utf-8')

    class Meta(MetaCore):
        db_table = 'languages'
        ordering = ['name']

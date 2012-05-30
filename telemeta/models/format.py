# -*- coding: utf-8 -*-
# Copyright (C) 2010-2012 Parisson SARL

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

import re
import mimetypes
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from telemeta.models.core import *
from telemeta.util.unaccent import unaccent_icmp
from telemeta.models.location import *
from telemeta.models.system import *
from telemeta.models.query import *
from telemeta.models.instrument import *
from telemeta.models.enum import *
from telemeta.models.language import *
from telemeta.models.media import *
from django.db import models


class Format(ModelCore):
    """ Physical format object as proposed by the LAM"""

    element_type          = 'format'

    item                  = ForeignKey('MediaItem', related_name="format", verbose_name = _("item"),
                                       blank=True, null=True, on_delete=models.SET_NULL)
    physical_format       = WeakForeignKey(PhysicalFormat, related_name="format",
                                     verbose_name = _("physical format"))
    original_code         = CharField(_('original code'))
    original_number       = CharField(_('original number'))
    original_status       = CharField(_('original status'))
    original_state        = TextField(_('technical properties / conservation state'))
    original_comments     = TextField(_('comments / notes'))
    original_location     = ForeignKey('Location', related_name="format",
                                       verbose_name = _("original location"),
                                       blank=True, null=True, on_delete=models.SET_NULL)
    original_channels     = WeakForeignKey(NumberOfChannels, related_name="format",
                                        verbose_name = _("number of channels"))
    original_audio_quality = TextField(_('audio quality'))
    recording_system      = CharField(_('recording system'))

    # Tapes
    tape_wheel_diameter = WeakForeignKey(TapeWheelDiameter, related_name="format",
                                        verbose_name = _("tape wheel diameter (cm)"))
    tape_thickness      = CharField(_('tape thickness (um)'))
    tape_speed          = WeakForeignKey(TapeSpeed, related_name="format",
                                        verbose_name = _("tape speed (cm/s)"))
    tape_vendor         = WeakForeignKey(TapeVendor, related_name="format",
                                        verbose_name = _("tape vendor"))
    tape_reference      = CharField(_('tape reference'))
    sticker_presence    = BooleanField(_('sticker presence'))

    class Meta(MetaCore):
        db_table = 'media_formats'
        verbose_name = _('format')

    def __unicode__(self):
        if self.physical_format:
            return ' - '.join([self.physical_format.value, self.original_code,
                               self.item.public_id])
        else:
            return 'Unknown'

    @property
    def public_id(self):
        return self.original_code

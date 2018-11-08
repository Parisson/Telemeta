# -*- coding: utf-8 -*-
# Copyright (C) 2010-2012 Parisson SARL

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
# Authors:
#          Guillaume Pellerin <yomguy@parisson.com>

import re
import mimetypes
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from telemeta.models.core import *
from telemeta.util.unaccent import unaccent_icmp
from telemeta.models.enum import *
from telemeta.models.language import *
from django.db import models

ITEM_ORIGINAL_STATUS_CHOICES = (('None', _('None')), ('original format', _('original format')), ('copies', _('copies')), ('secondary edition', _('secondary edition')))

class Format(ModelCore):
    """ Physical format object as proposed by the LAM"""

    element_type          = 'format'

    item                  = ForeignKey('MediaItem', related_name="format", verbose_name = _("item"),
                                       blank=True, null=True, on_delete=models.SET_NULL)
    original_code         = CharField(_('original code'))
    #original_status       = CharField(_('original status'))
    original_status       = CharField(_('original status'), choices=ITEM_ORIGINAL_STATUS_CHOICES, max_length=20, default="None")
    #original_location     = ForeignKey('Organization', related_name="format",
    #original_location     = ForeignKey('Location', related_name="format",
    #                                   verbose_name = _("original location"),
    #                                   blank=True, null=True, on_delete=models.SET_NULL)
    original_location     = WeakForeignKey(ConservationSite, related_name="format", verbose_name=_('conservation site'))
    physical_format       = WeakForeignKey(PhysicalFormat, related_name="format",
                                     verbose_name = _("physical format"))
    tape_vendor         = WeakForeignKey(TapeVendor, related_name="format",
                                        verbose_name = _("tape vendor"))
    tape_reference      = CharField(_('tape reference'))
    sticker_presence    = BooleanField(_('sticker presence'))
    tape_thickness      = CharField(_('tape thickness (um)'))
    tape_wheel_diameter = WeakForeignKey(TapeWheelDiameter, related_name="format",
                                        verbose_name = _("tape wheel diameter (cm)"))
    original_state        = TextField(_('technical properties / conservation state'))
    recording_system      = CharField(_('recording system'))
    original_audio_quality = TextField(_('audio quality'))


    original_number       = CharField(_('original number'))
    original_comments     = TextField(_('comments / notes'))
    original_channels     = WeakForeignKey(NumberOfChannels, related_name="format",
                                        verbose_name = _("number of channels"))

    # Tapes
    tape_speed          = WeakForeignKey(TapeSpeed, related_name="format",
                                        verbose_name = _("tape speed (cm/s)"))

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

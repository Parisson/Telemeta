# -*- coding: utf-8 -*-

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
# Authors: Anas Ghrab <anas.ghrab@gmail.com>

from __future__ import division
from django.db import models
from django.utils.translation import ugettext_lazy as _

class Authority(models.Model):
    "Describe an autority"

    # Main Informations
    first_name            = CharField(_('firstname'))
    last_name             = CharField(_('lastname'))

    class Meta:
        db_table = 'media_authority'
        verbose_name = _('authority')

    def __str__(self):
        return '%s %s' % (self.prenom, self.nom)

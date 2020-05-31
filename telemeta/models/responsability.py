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
from telemeta.models.item import *
from telemeta.models.collection import *

class Authority(models.Model):
    "Describe an autority"

    first_name            = models.CharField(_('firstname'), max_length=50, help_text=_('First name in original language'))
    last_name             = models.CharField(_('lastname'), max_length=50, help_text=_('Last name in original language'))
    first_name_lat        = models.CharField(_('firstname_lat'), max_length=50, null=True, blank=True, help_text=_('First name in latin characters, usage form'))
    last_name_lat         = models.CharField(_('lastname_lat'), max_length=50, null=True, blank=True, help_text=_('Last name in latin character, usage form'))
    first_name_translit   = models.CharField(_('firstname_translit'), max_length=50, null=True, blank=True, help_text=_('First name transliterated'))
    last_name_translit    = models.CharField(_('lastname_translit'), max_length=50, null=True, blank=True, help_text=_('Last name transliterated'))
    birth                 = models.DateField(_('birth'), null=True, blank=True, help_text=_('YYYY-MM-DD'))
    death                 = models.DateField(_('death'), null=True, blank=True, help_text=_('YYYY-MM-DD'))
    biography             = models.TextField(_('biography'), null=True, blank=True)
    isni                  = models.PositiveIntegerField(_('isni'), null=True, blank=True, help_text=_('International Standard Name Identifier'))
    #photo                 =

    class Meta:
        db_table = 'media_authority'
        verbose_name = _('authority')
        verbose_name_plural = _('authorities')

    def __str__(self):
        return '%s %s' % (self.prenom, self.nom)

class Role(models.Model):
    "Describe a role related to items"

    intitule            = models.CharField(_('role'), max_length=50, help_text=_('List of roles'))

    class Meta:
        db_table = 'media_role'
        verbose_name = _('role')
        verbose_name_plural = _('roles')

    def __str__(self):
        return '%s %s' % (self.intitule)

class Responsability(models.Model):
    "Describe a responsability in making an item"

    authority            = models.ForeignKey('Authority', on_delete = models.CASCADE)
    role                 = models.ForeignKey('Role', on_delete = models.CASCADE)
    item                 = models.ForeignKey('MediaItem', on_delete = models.CASCADE)
    collection           = models.ForeignKey('MediaCollection', on_delete = models.CASCADE)

    class Meta:
        db_table = 'media_responsability'
        verbose_name = _('responsability')
        verbose_name_plural = _('responsabilites')

    def __str__(self):
        return '%s %s' % (self.authority, self.role)

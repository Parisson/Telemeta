# -*- coding: utf-8 -*-
# Copyright (C) 2007-2010 Samalyse SARL
# Copyright (C) 2010-2011 Parisson SARL

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

from django.contrib.auth.models import User
from telemeta.models.core import *
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import ugettext_lazy as _
import django.db.models as models
from django.forms import ModelForm


class Revision(ModelCore):
    "Revision made by user"

    ELEMENT_TYPE_CHOICES = (('collection', 'collection'), ('item', 'item'), ('part', 'part'), ('marker', 'marker'), ('media', 'media'), ('fonds', 'fonds'), ('corpus', 'corpus'))
    CHANGE_TYPE_CHOICES  = (('import', 'import'), ('create', 'create'), ('update', 'update'), ('delete','delete'))

    element_type         = CharField(_('element type'), choices=ELEMENT_TYPE_CHOICES, max_length=16, required=True)
    element_id           = IntegerField(_('element identifier'), required=True)
    change_type          = CharField(_('modification type'), choices=CHANGE_TYPE_CHOICES, max_length=16, required=True)
    time                 = DateTimeField(_('time'), auto_now_add=True)
    user                 = ForeignKey(User, db_column='username', related_name="revisions", verbose_name=_('user'))

    @classmethod
    def touch(cls, element, user):
        "Create or update a revision"
        revision = cls(element_type=element.element_type, element_id=element.pk, user=user, change_type='create')
        if element.pk:
            try:
                element.__class__.objects.get(pk=element.pk)
            except ObjectDoesNotExist:
                pass
            else:
                revision.change_type = 'update'

        revision.save()
        return revision

    def __str__(self):
        return str(self.time) + ' : ' + self.element_type + ' : ' + str(self.element_id)

    class Meta(MetaCore):
        db_table = 'revisions'
        ordering = ['-time']


class UserProfile(models.Model):
    "User profile extension"

    user            = ForeignKey(User, unique=True, required=True)
    institution     = CharField(_('Institution'))
    department      = CharField(_('Department'))
    attachment      = CharField(_('Attachment'))
    function        = CharField(_('Function'))
    address         = TextField(_('Address'))
    telephone       = CharField(_('Telephone'))
    expiration_date = DateField(_('Expiration_date'))

    class Meta(MetaCore):
        db_table = 'profiles'
        permissions = (("can_view_users_and_profiles", "Can view other users and any profile"),)


class Criteria(ModelCore):
    "Search criteria"

    element_type = 'search_criteria'

    key = CharField(_('key'), required=True)
    value = CharField(_('value'), required=True)

    class Meta(MetaCore):
        db_table = 'search_criteria'


class Search(ModelCore):
    "Keywork search"

    element_type = 'search'

    username = ForeignKey(User, related_name="searches", db_column="username")
    date = DateTimeField(_('date'), auto_now_add=True)
    description = CharField(_('Description'))
    criteria = models.ManyToManyField(Criteria, related_name="search", verbose_name=_('criteria'), blank=True, null=True)

    class Meta(MetaCore):
        db_table = 'searches'
        ordering = ['-date']

    def __unicode__(self):
        return ' - '.join([self.username.username, unicode(self.date), ' - '.join([c.key for c in self.criteria.all()])])

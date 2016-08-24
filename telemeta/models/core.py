# -*- coding: utf-8 -*-
#
# Copyright (C) 2007-2010 Samalyse SARL
# Copyright (C) 2010-2011 Parisson SARL
#
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
#          Guillaume Pellerin <yomguy@parisson.com>


import datetime
import mimetypes
import re, os, random

from django import forms
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.core import exceptions
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.core.urlresolvers import reverse, reverse_lazy
from django.db import models
from django.db.models import Q, URLField
from django.db.models.fields import FieldDoesNotExist
from django.forms.models import model_to_dict
from django.utils.translation import ugettext
from django.utils.translation import ugettext_lazy as _
from telemeta.models.utils import *
from telemeta.models.fields import *
from telemeta.util.kdenlive_session import *
from telemeta.util.unaccent import unaccent_icmp
from xml.dom.minidom import getDOMImplementation
from dirtyfields import DirtyFieldsMixin

PUBLIC_ACCESS_CHOICES = (('none', _('none')), ('metadata', _('metadata')),
                         ('mixed', _('mixed')), ('full', _('full')))

public_extra_types = {
    '.webm': 'video/webm',
    '.mp4': 'video/mp4',
}

private_extra_types = {
    '.eaf': 'text/xml',  # ELAN Annotation Format
    '.trs':  'text/xml', # Trancriber Annotation Format
    '.svl':  'text/xml',  # Sonic Visualiser layer file
    '.TextGrid': 'text/praat-textgrid',  # Praat TextGrid annotation file
}

for ext,mime_type in public_extra_types.items():
    mimetypes.add_type(mime_type, ext)

for ext,mime_type in private_extra_types.items():
    mimetypes.add_type(mime_type, ext)

app_name = 'telemeta'

strict_code = getattr(settings, 'TELEMETA_STRICT_CODE', False)


class EnhancedQuerySet(models.query.QuerySet):
    """QuerySet with added functionalities such as WeakForeignKey handling"""

    def delete(self):
        CHUNK=1024
        objects = self.model._meta.get_all_related_objects()
        ii = self.count()
        values = self.values_list('pk')
        for related in objects:
            i = 0
            while i < ii:
                ids = [v[0] for v in values[i:i + CHUNK]]
                filter = {related.field.name + '__pk__in': ids}
                q = related.model.objects.filter(**filter)
                if isinstance(related.field, WeakForeignKey):
                    update = {related.field.name: None}
                    q.update(**update)
                else:
                    q.delete()

                i += CHUNK

        super(EnhancedQuerySet, self).delete()


class EnhancedManager(models.Manager):
    """Manager which is bound to EnhancedQuerySet"""
    def get_query_set(self):
        return EnhancedQuerySet(self.model)


class EnhancedModel(models.Model):
    """Base model class with added functionality. See EnhancedQuerySet"""

    objects = EnhancedManager()

    def delete(self):
        if not self.pk:
            raise Exception("Can't delete without a primary key")
        self.__class__.objects.filter(pk=self.pk).delete()

    class Meta:
        abstract = True


class ModelCore(EnhancedModel, DirtyFieldsMixin):

    @classmethod
    def required_fields(cls):
        required = []
        for field in cls._meta.fields:
            if not field.blank:
                required.append(field)
        return required

    def save(self, force_insert=False, force_update=False, *args, **kwargs):
        required = self.required_fields()
        for field in required:
            if not getattr(self, field.name):
                raise RequiredFieldError(self, field)
        super(ModelCore, self).save(force_insert, force_update, *args, **kwargs)

    @classmethod
    def get_dom_name(cls):
        "Convert the class name to a DOM element name"
        clsname = cls.__name__
        return clsname[0].lower() + clsname[1:]

    @staticmethod
    def get_dom_field_name(field_name):
        "Convert the class name to a DOM element name"
        tokens = field_name.split('_')
        name = tokens[0]
        for t in tokens[1:]:
            name += t[0].upper() + t[1:]
        return name

    def to_dom(self):
        "Return the DOM representation of this media object"
        impl = getDOMImplementation()
        root = self.get_dom_name()
        doc = impl.createDocument(None, root, None)
        top = doc.documentElement
        top.setAttribute("id", str(self.pk))
        fields = self.to_dict()
        for name, value in fields.iteritems():
            element = doc.createElement(self.get_dom_field_name(name))
            if isinstance(value, EnhancedModel):
                element.setAttribute('key', str(value.pk))
            value = unicode(value)
            element.appendChild(doc.createTextNode(value))
            top.appendChild(element)
        return doc

    def to_dict(self):
        "Return model fields as a dict of name/value pairs"
        fields_dict = {}
        for field in self._meta.fields:
            fields_dict[field.name] = getattr(self, field.name)
        return fields_dict

    def to_list(self):
        "Return model fields as a list"
        fields_list = []
        for field in self._meta.fields:
            fields_list.append({'name': field.name, 'value': unicode(getattr(self, field.name))})
        return fields_list

    @classmethod
    def field_label(cls, field_name=None):
        if field_name:
            try:
                return cls._meta.get_field(field_name).verbose_name
            except FieldDoesNotExist:
                try:
                    return getattr(cls, field_name).verbose_name
                except AttributeError:
                    return field_name
        else:
            return cls._meta.verbose_name

    class Meta:
        abstract = True


class MetaCore:
    app_label = 'telemeta'



class CoreQuerySet(EnhancedQuerySet):
    "Base class for all query sets"

    def none(self): # redundant with none() in recent Django svn
        "Return an empty result set"
        return self.extra(where = ["0 = 1"])

    def word_search(self, field, pattern):
        return self.filter(word_search_q(field, pattern))

    def _by_change_time(self, type, from_time = None, until_time = None):
        "Search between two revision dates"
        table = self.model._meta.db_table
        where = []
        if from_time:
            where.append("revisions.time >= '%s'" % from_time.strftime('%Y-%m-%d %H:%M:%S'))
        if until_time:
            where.append("revisions.time <= '%s'" % until_time.strftime('%Y-%m-%d %H:%M:%S'))

        qs = self
        if where:
            where.extend(["revisions.element_type = '%s'" % type, "revisions.element_id = %s.id" % table])
            qs = qs.extra(where = [" AND ".join(where)],
                            tables = ['revisions']).distinct()
        return qs


class CoreManager(EnhancedManager):
    "Base class for all models managers"

    def none(self, *args, **kwargs):
        ""
        return self.get_query_set().none(*args, **kwargs)

    def get(self, **kwargs):
        if kwargs.has_key('public_id'):
            try:
                args = kwargs.copy()
                args['code'] = kwargs['public_id']
                args.pop('public_id')
                return super(CoreManager, self).get(**args)
            except ObjectDoesNotExist:
                args = kwargs.copy()
                args['id'] = kwargs['public_id']
                args.pop('public_id')
                return super(CoreManager, self).get(**args)

        return super(CoreManager, self).get(**kwargs)

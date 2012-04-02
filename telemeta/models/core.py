# -*- coding: utf-8 -*-
#
# Copyright (C) 2007-2010 Samalyse SARL
# Copyright (C) 2010-2011 Parisson SARL
#
# This software is a computer program whose purpose is to backup, analyse,
# transcode and stream any audio content with its metadata over a web frontend.
#
# This software is governed by the CeCILL  license under French law and
# abiding by the rules of distribution of free software.  You can  use,
# modify and/ or redistribute the software under the terms of the CeCILL
# license as circulated by CEA, CNRS and INRIA at the following URL
# "http://www.cecill.info".
#
# As a counterpart to the access to the source code and  rights to copy,
# modify and redistribute granted by the license, users are provided only
# with a limited warranty  and the software's author,  the holder of the
# economic rights,  and the successive licensors  have only  limited
# liability.
#
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
#
# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL license and that you accept its terms.
#
# Authors: Olivier Guilyardi <olivier@samalyse.com>
#          Guillaume Pellerin <yomguy@parisson.com>

__all__ = ['ModelCore', 'MetaCore', 'DurationField', 'Duration', 'WeakForeignKey',
           'EnhancedModel', 'CharField', 'TextField', 'IntegerField', 'BooleanField',
           'DateTimeField', 'FileField', 'ForeignKey', 'FloatField', 'DateField',
           'RequiredFieldError', 'CoreQuerySet', 'CoreManager', 'word_search_q']

from django.core import exceptions
from django import forms
from xml.dom.minidom import getDOMImplementation
from django.db.models.fields import FieldDoesNotExist
from django.db.models import Q
from django.db import models
import datetime
from django.utils.translation import ugettext_lazy as _
import re
from django.core.exceptions import ObjectDoesNotExist
from south.modelsinspector import add_introspection_rules

class Duration(object):
    """Represent a time duration"""
    def __init__(self, *args, **kwargs):
        if len(args) and isinstance(args[0], datetime.timedelta):
            self._delta = datetime.timedelta(days=args[0].days, seconds=args[0].seconds)
        else:
            self._delta = datetime.timedelta(*args, **kwargs)

    def __decorate(self, method, other):
        if isinstance(other, Duration):
            res = method(other._delta)
        else:
            res = method(other)
        if type(res) == datetime.timedelta:
            return Duration(res)

        return res

    def __add__(self, other):
        return self.__decorate(self._delta.__add__, other)

    def __nonzero__(self):
        return self._delta.__nonzero__()

    def __str__(self):
        hours   = self._delta.days * 24 + self._delta.seconds / 3600
        minutes = (self._delta.seconds % 3600) / 60
        seconds = self._delta.seconds % 60

        return "%.2d:%.2d:%.2d" % (hours, minutes, seconds)

    @staticmethod
    def fromstr(str):
        if not str:
            return Duration()

        test = re.match('^([0-9]+)(?::([0-9]+)(?::([0-9]+))?)?$', str)
        if test:
            groups = test.groups()
            try:
                hours = minutes = seconds = 0
                if groups[0]:
                    hours = int(groups[0])
                    if groups[1]:
                        minutes = int(groups[1])
                        if groups[2]:
                            seconds = int(groups[2])

                return Duration(hours=hours, minutes=minutes, seconds=seconds)
            except TypeError:
                print groups
                raise
        else:
            raise ValueError("Malformed duration string: " + str)

    def as_seconds(self):
        return self._delta.days * 24 * 3600 + self._delta.seconds

def normalize_field(args, default_value=None):
    """Normalize field constructor arguments, so that the field is marked blank=True
       and has a default value by default.

       This behaviour can be disabled by passing the special argument required=True.

       The default value can also be overriden with the default=value argument.
       """
    required = False
    if args.has_key('required'):
        required = args['required']
        args.pop('required')

    args['blank'] = not required

    if not required:
        if not args.has_key('default'):
            if args.get('null'):
                args['default'] = None
            elif default_value is not None:
                args['default'] = default_value

    return args

# The following is based on Django TimeField
class DurationField(models.Field):
    """Duration Django model field. Essentially the same as a TimeField, but
    with values over 24h allowed.

    The constructor arguments are also normalized with normalize_field().
    """

    description = _("Duration")

    __metaclass__ = models.SubfieldBase

    default_error_messages = {
        'invalid': _('Enter a valid duration in HH:MM[:ss] format.'),
    }

    def __init__(self, *args, **kwargs):
        super(DurationField, self).__init__(*args, **normalize_field(kwargs, '00:00'))

    def db_type(self):
        return 'int'

    def to_python(self, value):
        if value is None:
            return None
        if isinstance(value, int) or isinstance(value, long):
            return Duration(seconds=value)
        if isinstance(value, datetime.time):
            return Duration(hours=value.hour, minutes=value.minute, seconds=value.second)
        if isinstance(value, datetime.datetime):
            # Not usually a good idea to pass in a datetime here (it loses
            # information), but this can be a side-effect of interacting with a
            # database backend (e.g. Oracle), so we'll be accommodating.
            return self.to_python(value.time())
        else:
            value = str(value)
        try:
            return Duration.fromstr(value)
        except ValueError:
            raise exceptions.ValidationError(self.error_messages['invalid'])

    def get_prep_value(self, value):
        return self.to_python(value)

    def get_db_prep_value(self, value, connection=None, prepared=False):
        # Casts times into the format expected by the backend
        try:
            return value.as_seconds()
        except:
            return value

    def value_to_string(self, obj):
        val = self._get_val_from_obj(obj)
        if val is None:
            data = ''
        else:
            data = unicode(val)
        return data

    def formfield(self, **kwargs):
        defaults = {'form_class': forms.CharField}
        defaults.update(kwargs)
        return super(DurationField, self).formfield(**defaults)

class ForeignKey(models.ForeignKey):
    """The constructor arguments of this ForeignKey are normalized
    with normalize_field(), however the field is marked required by default
    unless it is allowed to be null."""

    def __init__(self, to, **kwargs):
        if not kwargs.has_key('required'):
            if not kwargs.get('null'):
                kwargs['required'] = True

        super(ForeignKey, self).__init__(to, **normalize_field(kwargs, 0))

class WeakForeignKey(ForeignKey):
    """A weak foreign key is the same as foreign key but without cascading
    delete. Instead the reference is set to null when the referenced record
    get deleted. This emulates the ON DELETE SET NULL sql behaviour.

    This field is automatically allowed to be null, there's no need to pass
    null=True.

    The constructor arguments are normalized with normalize_field() by the
    parent ForeignKey

    Warning: must be used in conjunction with EnhancedQuerySet, EnhancedManager,
    and EnhancedModel
    """
    def __init__(self, to, **kwargs):
        kwargs['null'] = True
        super(WeakForeignKey, self).__init__(to, **kwargs)

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

class CharField(models.CharField):
    """This is a CharField with a default max_length of 250.

       The arguments are also normalized with normalize_field()"""

    def __init__(self, *args, **kwargs):
        if not kwargs.has_key('max_length'):
            kwargs['max_length'] = 250

        super(CharField, self).__init__(*args, **normalize_field(kwargs, ''))

class IntegerField(models.IntegerField):
    """IntegerField normalized with normalize_field()"""

    def __init__(self, *args, **kwargs):
        super(IntegerField, self).__init__(*args, **normalize_field(kwargs, 0))

class BooleanField(models.BooleanField):
    """BooleanField normalized with normalize_field()"""

    def __init__(self, *args, **kwargs):
        super(BooleanField, self).__init__(*args, **normalize_field(kwargs, False))

class TextField(models.TextField):
    """TextField normalized with normalize_field()"""

    def __init__(self, *args, **kwargs):
        super(TextField, self).__init__(*args, **normalize_field(kwargs, ''))

class DateTimeField(models.DateTimeField):
    """DateTimeField normalized with normalize_field(). This field is allowed to
    be null by default unless null=False is passed"""

    def __init__(self, *args, **kwargs):
        if not kwargs.has_key('null'):
            kwargs['null'] = True
        super(DateTimeField, self).__init__(*args, **normalize_field(kwargs))

class FileField(models.FileField):
    """FileField normalized with normalize_field()"""

    def __init__(self, *args, **kwargs):
        super(FileField, self).__init__(*args, **normalize_field(kwargs, ''))

class FloatField(models.FloatField):
    """FloatField normalized with normalize_field()"""

    def __init__(self, *args, **kwargs):
        super(FloatField, self).__init__(*args, **normalize_field(kwargs, 0))

class DateField(models.DateField):
    """DateField normalized with normalize_field(). This field is allowed to
    be null by default unless null=False is passed"""

    def __init__(self, *args, **kwargs):
        if not kwargs.has_key('null'):
            kwargs['null'] = True
        super(DateField, self).__init__(*args, **normalize_field(kwargs))

class RequiredFieldError(Exception):
    def __init__(self, model, field):
        self.model = model
        self.field = field
        super(Exception, self).__init__('%s.%s is required' % (model._meta.object_name, field.name))

class ModelCore(EnhancedModel):

    @classmethod
    def required_fields(cls):
        required = []
        for field in cls._meta.fields:
            if not field.blank:
                required.append(field)
        return required

    def save(self, force_insert=False, force_update=False):
        required = self.required_fields()
        for field in required:
            if not getattr(self, field.name):
                raise RequiredFieldError(self, field)
        super(ModelCore, self).save(force_insert, force_update)

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
            fields_list.append({'name': field.name, 'value': getattr(self, field.name)})
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

def word_search_q(field, pattern):
    words = re.split("[ .*-]+", pattern)
    q = Q()
    for w in words:
        if len(w) >= 3:
            kwargs = {field + '__icontains': w}
            q &= Q(**kwargs)

    return q

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


# South introspection rules
add_introspection_rules([], ["^telemeta\.models\.core\.CharField"])
add_introspection_rules([], ["^telemeta\.models\.core\.TextField"])
add_introspection_rules([], ["^telemeta\.models\.core\.FileField"])
add_introspection_rules([], ["^telemeta\.models\.core\.IntegerField"])
add_introspection_rules([], ["^telemeta\.models\.core\.BooleanField"])
add_introspection_rules([], ["^telemeta\.models\.core\.DateTimeField"])
add_introspection_rules([], ["^telemeta\.models\.core\.DateField"])
add_introspection_rules([], ["^telemeta\.models\.core\.FloatField"])
add_introspection_rules([], ["^telemeta\.models\.core\.DurationField"])
add_introspection_rules([], ["^telemeta\.models\.core\.ForeignKey"])
add_introspection_rules([], ["^telemeta\.models\.core\.WeakForeignKey"])


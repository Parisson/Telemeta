# -*- coding: utf-8 -*-
#
# Copyright (C) 2007-2010 Samalyse SARL
# Copyright (C) 2010-2015 Parisson SARL
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

from __future__ import division

__all__ = ['DurationField', 'Duration', 'WeakForeignKey',
           'CharField', 'TextField', 'IntegerField', 'BooleanField',
           'DateTimeField', 'FileField', 'ForeignKey', 'FloatField', 'DateField',
           'RequiredFieldError',]

import datetime, re
from django import forms
from django.db import models
from django.utils.translation import ugettext_lazy as _
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

    def __unicode__(self):
        return self.__str__()

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


class DurationField(models.Field):
    """Duration Django model field based on Django TimeField.
    Essentially the same as a TimeField, but with values over 24h allowed.

    The constructor arguments are also normalized with normalize_field().
    """

    description = _("Duration")

    __metaclass__ = models.SubfieldBase

    default_error_messages = {
        'invalid': _('Enter a valid duration in HH:MM[:ss] format.'),
    }

    def __init__(self, *args, **kwargs):
        super(DurationField, self).__init__(*args, **normalize_field(kwargs, '0'))

    def db_type(self, connection):
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



# South introspection rules
add_introspection_rules([], ["^telemeta\.models\.fields\.CharField"])
add_introspection_rules([], ["^telemeta\.models\.fields\.TextField"])
add_introspection_rules([], ["^telemeta\.models\.fields\.FileField"])
add_introspection_rules([], ["^telemeta\.models\.fields\.IntegerField"])
add_introspection_rules([], ["^telemeta\.models\.fields\.BooleanField"])
add_introspection_rules([], ["^telemeta\.models\.fields\.DateTimeField"])
add_introspection_rules([], ["^telemeta\.models\.fields\.DateField"])
add_introspection_rules([], ["^telemeta\.models\.fields\.FloatField"])
add_introspection_rules([], ["^telemeta\.models\.fields\.DurationField"])
add_introspection_rules([], ["^telemeta\.models\.fields\.ForeignKey"])
add_introspection_rules([], ["^telemeta\.models\.fields\.WeakForeignKey"])


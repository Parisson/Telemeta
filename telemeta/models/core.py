# -*- coding: utf-8 -*-
# Copyright (C) 2007-2010 Samalyse SARL

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

from django.db import models
import datetime
from django.utils.translation import ugettext_lazy as _
import re

class Duration(object):

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
            
# The following is based on Django TimeField
class DurationField(models.Field):
    description = _("Duration")

    __metaclass__ = models.SubfieldBase

    default_error_messages = {
        'invalid': _('Enter a valid duration in HH:MM[:ss[.uuuuuu]] format.'),
    }

    def get_internal_type(self):
        return 'TimeField'

    def to_python(self, value):
        if value is None:
            return None
        if isinstance(value, datetime.time):
            return Duration(hours=value.hour, minutes=value.minute, seconds=value.second)
        if isinstance(value, datetime.datetime):
            # Not usually a good idea to pass in a datetime here (it loses
            # information), but this can be a side-effect of interacting with a
            # database backend (e.g. Oracle), so we'll be accommodating.
            return self.to_python(value.time())

        try:
            return Duration.fromstr(value)
        except ValueError:
            raise exceptions.ValidationError(self.error_messages['invalid'])
            
    def get_prep_value(self, value):
        return self.to_python(value)

    def get_db_prep_value(self, value, connection, prepared=False):
        # Casts times into the format expected by the backend
        return unicode(value)

    def value_to_string(self, obj):
        val = self._get_val_from_obj(obj)
        if val is None:
            data = ''
        else:
            data = unicode(val)
        return data

    def formfield(self, **kwargs):
        defaults = {'form_class': forms.TimeField}
        defaults.update(kwargs)
        return super(DurationField, self).formfield(**defaults)
            

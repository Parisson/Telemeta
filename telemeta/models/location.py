# -*- coding: utf-8 -*-
# Copyright (C) 2007 Samalyse SARL

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

from telemeta.models.core import *
from telemeta.util.unaccent import unaccent
import re
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _
from telemeta.models.query import *
from django.forms import ModelForm


class Location(ModelCore):
    "Locations"
    OTHER_TYPE  = 0
    CONTINENT   = 1
    COUNTRY     = 2
    TYPE_CHOICES     = ((COUNTRY, _('country')), (CONTINENT, _('continent')), (OTHER_TYPE, _('other')))

    name             = CharField(_('name'), unique=True, max_length=150, required=True)
    type             = IntegerField(_('type'), choices=TYPE_CHOICES, default=OTHER_TYPE, db_index=True)
    complete_type    = ForeignKey('LocationType', related_name="locations", verbose_name=_('complete type'))
    current_location = WeakForeignKey('self', related_name="past_names",
                                      verbose_name=_('current location'))
    latitude         = FloatField(null=True)
    longitude        = FloatField(null=True)
    is_authoritative = BooleanField(_('authoritative'))

    objects = LocationManager()

    def items(self):
        from telemeta.models import MediaItem
        return MediaItem.objects.by_location(self)

    def collections(self):
        from telemeta.models import MediaCollection
        return MediaCollection.objects.by_location(self)

    def ancestors(self, direct=False):
        q = Q(descendant_relations__location=self)
        if direct:
            q &= Q(descendant_relations__is_direct=True)
        return Location.objects.filter(q)

    def descendants(self, direct=False):
        q = Q(ancestor_relations__ancestor_location=self)
        if direct:
            q &= Q(ancestor_relations__is_direct=True)
        return Location.objects.filter(q)

    def apparented(self):
        return Location.objects.filter(
                Q(pk=self.id) |
                Q(ancestor_relations__ancestor_location=self) |
                Q(current_location=self.id)).distinct()

    def add_child(self, other):
        LocationRelation.objects.create(location=other, ancestor_location=self, is_direct=True)
        for location in self.ancestors():
            #FIXME: might raise Duplicate Entry
            LocationRelation.objects.create(location=other, ancestor_location=location)

    def add_parent(self, other):
        LocationRelation.objects.create(location=self, ancestor_location=other, is_direct=True)
        for location in self.descendants():
            #FIXME: might raise Duplicate Entry
            LocationRelation.objects.create(location=location, ancestor_location=other)

    def countries(self):
        if self.type == self.COUNTRY:
            return Location.objects.filter(pk=self.id)
        return self.ancestors().filter(type=self.COUNTRY)

    def continents(self):
        if self.type == self.CONTINENT:
            return Location.objects.filter(pk=self.id)
        return self.ancestors().filter(type=self.CONTINENT)

    class Meta(MetaCore):
        db_table = 'locations'
        verbose_name = _('location')
        verbose_name_plural = _('locations')
        ordering = ['name']

    def __unicode__(self):
        return self.name

    def flatname(self):
        if self.type != self.COUNTRY and self.type != self.CONTINENT:
            raise Exception("Flat names are only supported for countries and continents")

        map = Location.objects.flatname_map()
        for flatname in map:
            if self.id == map[flatname]:
                return flatname

        return None

    def paths(self):
        #FIXME: need to handle multiple (polyhierarchical) paths
        path = []
        location = self
        while location:
            path.append(location)
            try:
                location = location.ancestors(direct=True)[0]
            except IndexError:
                location = None
        return [path]

    def fullnames(self):
        names = []
        for path in self.paths():
            names.append(u', '.join([unicode(l) for l in path]))
        return names

    def listnames(self):
        names = []
        for path in self.paths():
            for l in path:
                names.append(unicode(l))
        return names


class LocationType(ModelCore):
    "Location types"
    code = CharField(_('identifier'), max_length=64, unique=True, required=True)
    name = CharField(_('name'), max_length=150, required=True)

    def __unicode__(self):
        return self.name

    class Meta(MetaCore):
        db_table = 'location_types'
        ordering = ['name']
        verbose_name_plural = _('location types')

class LocationAlias(ModelCore):
    "Location aliases"
    location         = ForeignKey('Location', related_name="aliases", verbose_name=_('location'))
    alias            = CharField(_('alias'), max_length=150, required=True)
    is_authoritative = BooleanField(_('authoritative'))

    def __unicode__(self):
        return self.alias

    class Meta(MetaCore):
        db_table = 'location_aliases'
        unique_together = (('location', 'alias'),)
        verbose_name_plural = _('location aliases')
        ordering = ['alias']

class LocationRelation(ModelCore):
    "Location relations"
    location             = ForeignKey('Location', related_name="ancestor_relations", verbose_name=_('location'))
    ancestor_location    = ForeignKey('Location', related_name="descendant_relations",  verbose_name=_('ancestor location'))
    is_direct            = BooleanField(db_index=True)
    is_authoritative = BooleanField(_('authoritative'))

    class Meta(MetaCore):
        db_table = 'location_relations'
        unique_together = ('location', 'ancestor_location')
        ordering = ['ancestor_location__name']
        verbose_name_plural = _('location relations')

    def __unicode__(self):
        sep = ' > '
        if not self.is_direct:
            sep = ' >..> '
        return unicode(self.ancestor_location) + sep + unicode(self.location)


class LocationForm(ModelForm):
    class Meta:
        model = Location

    def __init__(self, *args, **kwds):
        super(LocationForm, self).__init__(*args, **kwds)
#        self.fields['name'].queryset = Location.objects.order_by('name')


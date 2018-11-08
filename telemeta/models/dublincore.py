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
# Author: Olivier Guilyardi <olivier@samalyse.com>

from telemeta.models.core import *
from telemeta.models.item import *
from telemeta.models.collection import *
from django.contrib.sites.models import Site
from django.conf import settings


class Resource(object):
    "Represent a Dublin Core resource"

    def __init__(self, *args):
        self.elements = []
        self.add(*args)

    def flatten(self):
        """Convert the resource to a dictionary with element names as keys.

        Warnings:
        - refinements are lost during this conversion,
        - if there are several occurences of the same element, only the first is
        used, others are lost.
        - all values are converted to strings
        """
        result = {}
        for element in self.elements:
            if not result.has_key(element.name):
                result[element.name] = unicode(element.value)
        return result

    def to_list(self):
        """Convert the resource to unqualified dublin core, as a list of the form:
           [(key, value), ...]"""
        result = []
        for element in self.elements:
            if isinstance(element.value, str):
                value = element.value.decode('utf8')
            else:
                value = element.value
            result.append((element.name, unicode(value)))
        return result

    def add(self, *elements):
        for e in elements:
            if isinstance(e, Element):
                if not e in self.elements:
                    self.elements.append(e)
            else:
                try:
                    iter(e)
                except TypeError:
                    raise Exception("add() only accepts elements or sequences of elements")

                self.add(*e)

    def __unicode__(self):
        dump = u''
        for e in self.elements:
            key = unicode(e.name)
            if e.refinement:
                key += u'.' + unicode(e.refinement)
            dump += u'%s:\t%s\n' % (key, unicode(e.value))
        return dump


class Element(object):
    "Represent a Dublin Core element"

    def __init__(self, name, value=None, refinement=None, related=None):
        self.name = name
        self.value = value
        self.refinement = refinement
        self.related = related

    def __eq__(self, other):
        return self.name == other.name and self.value == other.value and self.refinement == self.refinement

    def __ne__(self, other):
        return not (self == other)

    @staticmethod
    def multiple(name, values, refinement=None):
        elements = []
        if values:
            for v in values:
                elements.append(Element(name, v, refinement))
        return elements

class Date(Element):
    "Dublin Core date element formatted according to W3C-DTF or DCMI Period"

    def __init__(self, start, end=None, refinement=None):
        value = ''
        if start:
            value = start
        elif end:
            value = end
        else:
            value = ''
        if isinstance(value, long):
            # start is a year
            value = unicode(value) + '-01-01T00:00:00Z'
        elif value:
            value = value.strftime('%Y-%m-%dT%H:%M:%SZ')

        super(Date, self).__init__('date', value, refinement)

def media_access_rights(media):
    if media.public_access == 'full':
        return 'public'
    if media.public_access == 'metadata':
        return 'restricted'
    return 'private'

def media_identifier(media):
    sites = Site.objects.all()
    domain = sites[0].domain
    return 'http://' + domain + '/' + media.element_type + 's/' + unicode(media.id)

def media_generic_identifier(media):
    sites = Site.objects.all()
    domain = sites[0].domain
    return 'http://' + domain + '/' + media.element_type + '/' + unicode(media.id)

def express_collection(collection):
    "Express a collection as a Dublin Core resource"

    if collection.collector:
        creator = (Element('creator', collection.collector),
                   Element('contributor', collection.creator))
    else:
        creator = Element('creator', collection.creator)

    duration = max(collection.approx_duration, collection.computed_duration())
    parts = []
    for item in collection.items.all():
        id = media_identifier(item)
        if id:
            parts.append(Element('relation', id, 'hasPart', item))

    titles = [Element('title', collection.title),]
    if collection.alt_title:
        titles.append(Element('title', collection.alt_title))

    dates = []
    if collection.recorded_from_year or collection.recorded_to_year:
        dates.append(Date(collection.recorded_from_year, collection.recorded_to_year, refinement='created'))
    if collection.year_published:
        dates.append(Date(collection.year_published, refinement='issued'))

    resource = Resource(
        Element('identifier',       media_identifier(collection), related=collection),
        Element('identifier',       collection.public_id, related=collection),
        Element('type',             'Collection'),
        titles,
        creator,
        Element('contributor',      collection.metadata_author),
        Element.multiple('subject', settings.TELEMETA_SUBJECTS),
        Element('publisher',        collection.publisher),
        Element('publisher',        settings.TELEMETA_ORGANIZATION),
        dates,
        Element('rights',           collection.legal_rights, 'license'),
        Element('rights',           media_access_rights(collection), 'accessRights'),
        Element('format',           duration, 'extent'),
        Element('format',           collection.physical_format, 'medium'),
        parts
    )

    return resource

def express_item(item):
    "Express a media item as a Dublin Core resource"

    if item.collector:
        creator = (Element('creator', item.collector),
                   Element('contributor', item.collection.creator))
    elif item.collection.collector:
        creator = (Element('creator', item.collection.collector),
                   Element('contributor', item.collection.creator))
    else:
        creator = Element('creator', item.collection.creator)

    dates = []
    if item.recorded_from_date:
        dates.append(Date(item.recorded_from_date, item.recorded_to_date, refinement='created'))
    elif item.collection.recorded_from_year or item.collection.recorded_to_year:
        dates.append(Date(item.collection.recorded_from_year, item.collection.recorded_to_year, refinement='created'))
    if item.collection.year_published:
        dates.append(Date(item.collection.year_published, refinement='issued'))

    titles = []
    if item.title:
        title = item.title
    else:
        title = item.collection.title
        if item.track:
            title += u' - ' + item.track
    titles.append(Element('title', item.title))

    if item.alt_title:
        titles.append(Element('title', item.alt_title))

    try:
        analysis = MediaItemAnalysis.objects.get(item=item, analyzer_id='mime_type')
        mime_type = analysis.value
    except:
        mime_type = ''

    resource = Resource(
        Element('identifier',       media_identifier(item), related=item),
        Element('identifier',       item.public_id, related=item),
        Element('type',             'Sound'),
        titles,
        creator,
        Element('contributor',      item.collection.metadata_author),
        Element.multiple('subject', settings.TELEMETA_SUBJECTS),
        Element.multiple('subject', item.keywords()),
        Element('description',      item.context_comment, 'abstract'),
        Element('publisher',        item.collection.publisher),
        Element('publisher',        settings.TELEMETA_ORGANIZATION),
        dates,
        Element.multiple('coverage', item.location and item.location.listnames(), 'spatial'),
        Element('coverage',         item.location_comment, 'spatial'),
        Element('rights',           item.collection.legal_rights, 'license'),
        Element('rights',           media_access_rights(item.collection), 'accessRights'),
        Element('format',           max(item.approx_duration, item.computed_duration()), 'extent'),
        Element('format',           item.collection.physical_format, 'medium'),
        Element('format',           mime_type, 'MIME type'),
        Element('relation',         media_identifier(item.collection), 'isPartOf', item.collection)
    )

    return resource

def express_generic_resource(resource):
    "Express a media item as a Dublin Core resource"

    parts = []
    for child in resource.children.all():
        id = media_generic_identifier(child)
        if id:
            parts.append(Element('relation', id, 'hasPart', child))

    r = Resource(
        Element('identifier',       media_generic_identifier(resource), related=resource),
        Element('identifier',       resource.public_id, related=resource),
        Element('type',             resource.element_type),
        Element('title',            resource.title),
        Element('description',      resource.description),
        Element('publisher',        settings.TELEMETA_ORGANIZATION),
        parts
    )

    return r


def express_resource(res):
    if isinstance(res, MediaItem):
        return express_item(res)
    elif isinstance(res, MediaCollection):
        return express_collection(res)

    raise Exception("Invalid resource type")

def lookup_resource(media_id):
    try:
        id = media_id.split(':')
        type = id[-2]
        code = id[-1]
    except ValueError:
        raise MalformedMediaIdentifier("Media identifier must be in type:code format")

    if (type == 'collection') or (type == 'collections'):
        try:
            return MediaCollection.objects.get(code=code)
        except MediaCollection.DoesNotExist:
            return None
    elif (type == 'item') or (type == 'items'):
        try:
            return MediaItem.objects.get(code=code)
        except MediaItem.DoesNotExist:
            try:
                return MediaItem.objects.get(old_code=code)
            except MediaItem.DoesNotExist:
                try:
                    return MediaItem.objects.get(id=code)
                except MediaItem.DoesNotExist:
                    return None
    else:
        raise MalformedMediaIdentifier("No such type in media identifier: " + type)

class MalformedMediaIdentifier(Exception):
    pass


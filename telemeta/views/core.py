# -*- coding: utf-8 -*-
# Copyright (C) 2007-2010 Samalyse SARL
# Copyright (C) 2010-2017 Parisson SARL
# Copyright (C) 2010-2017 Guillaume Pellerin
# Copyright (C) 2010-2017 Thomas Fillon

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

# Authors: Olivier Guilyardi <olivier@samalyse.com>
#          Guillaume Pellerin <yomguy@parisson.com>
#          Thomas Fillon <thomas@parisson.com>

import re
import os
import sys
import csv
import time
import random
import datetime
import tempfile
import zipfile
import mimetypes
import json

from jsonrpc import jsonrpc_method

from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate, login
from django.template import RequestContext, loader
from django import template
from django.http import HttpResponse, HttpResponseRedirect, StreamingHttpResponse
# from django.http import FileResponse -> introduced in Django 1.7.4
from django.http import Http404
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.views.generic import *
from django.conf import settings
from django.contrib import auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.core.context_processors import csrf
from django.forms.models import modelformset_factory, inlineformset_factory
from django.contrib.auth.models import User
from django.utils.translation import ugettext
from django.contrib.auth.forms import UserChangeForm
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib.contenttypes.models import ContentType
from django.views.decorators.http import condition
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext_lazy
from django.forms.models import model_to_dict
from django.views.generic.edit import DeletionMixin, BaseDeleteView
from django.contrib.sites.models import Site
from django.template.defaultfilters import slugify


from telemeta.models import *

import telemeta.interop.oai as oai
from telemeta.interop.oaidatasource import TelemetaOAIDataSource
from telemeta.util.unaccent import unaccent
from telemeta.util.unaccent import unaccent_icmp
from telemeta.util.logger import Logger
from telemeta.util.unicode import UnicodeCSVWriter, Echo
from telemeta.cache import TelemetaCache
import pages
from telemeta.forms import *
import jqchat.models

# Model type definition
mods = {'item': MediaItem, 'collection': MediaCollection,
        'corpus': MediaCorpus, 'fonds': MediaFonds, 'marker': MediaItemMarker, }


class TelemetaBaseMixin(object):

    MEDIA_ROOT = getattr(settings, 'MEDIA_ROOT')
    CACHE_DIR = os.path.join(MEDIA_ROOT, 'cache')
    cache_data = TelemetaCache(getattr(settings, 'TELEMETA_DATA_CACHE_DIR', CACHE_DIR))
    cache_export = TelemetaCache(getattr(settings, 'TELEMETA_EXPORT_CACHE_DIR', os.path.join(CACHE_DIR, 'export')))
    cache_tmp = TelemetaCache(getattr(settings, 'FILE_UPLOAD_TEMP_DIR', os.path.join(MEDIA_ROOT, 'tmp')))


def serve_media(filename, content_type="", buffering=True):
    if not settings.DEBUG:
        return nginx_media_accel(filename, content_type=content_type,
                                 buffering=buffering)
    else:
        response = StreamingHttpResponse(stream_from_file(filename), content_type=content_type)
        response['Content-Disposition'] = 'attachment; ' + 'filename=' + filename
        return response


def nginx_media_accel(media_path, content_type="", buffering=True):
    """Send a protected media file through nginx with X-Accel-Redirect"""

    response = HttpResponse()
    url = settings.MEDIA_URL + os.path.relpath(media_path, settings.MEDIA_ROOT)
    filename = os.path.basename(media_path)
    response['Content-Disposition'] = "attachment; filename=%s" % (filename)
    response['Content-Type'] = content_type
    response['X-Accel-Redirect'] = url

    if not buffering:
        response['X-Accel-Buffering'] = 'no'
        #response['X-Accel-Limit-Rate'] = 524288

    return response


def render(request, template, data=None, mimetype=None):
    return render_to_response(template, data, context_instance=RequestContext(request),
                              mimetype=mimetype)


def stream_from_processor(decoder, encoder):
    pipe = decoder | encoder
    for chunk in pipe.stream():
        yield chunk

        
def stream_from_file(file):
    chunk_size = 0x100000
    f = open(file, 'r')
    while True:
        chunk = f.read(chunk_size)
        if not len(chunk):
            f.close()
            break
        yield chunk


def get_item_access(item, user):
    # Item access rules according to this workflow:
    # https://docs.google.com/spreadsheet/ccc?key=0ArKCjajoOT-fdDhJSDZoaUhqdDJvVkY5U3BXUWpNT0E#gid=0

    # Rolling publishing date : public access is automaticcaly given when time between recorded year
    # and current year is over the settings value PUBLIC_ACCESS_PERIOD and if item.auto_period_access == True

    if user.is_staff or user.is_superuser or user.has_perm('telemeta.can_play_all_items'):
        access = 'full'

    elif item.collection.public_access != 'mixed':
        if user.is_authenticated():
            if item.collection.public_access == 'metadata' and item.collection.auto_period_access:
                access = 'full'
            else:
                access = item.collection.public_access
        else:
            access = item.collection.public_access

    elif item.collection.public_access == 'mixed':
        if user.is_authenticated():
            if item.public_access == 'metadata' and item.auto_period_access:
                access = 'full'
            else:
                access = item.public_access
        else:
            access = item.public_access

    # Auto publish after a period given at settings.TELEMETA_PUBLIC_ACCESS_PERIOD
    if access != 'full' and access != 'none' and (item.auto_period_access or item.collection.auto_period_access):
        year_from = str(item.recorded_from_date).split('-')[0]
        year_to = str(item.recorded_to_date).split('-')[0]

        if year_from and not year_from == 0:
            year = year_from
        elif year_to and not year_to == 0:
            year = year_to
        else:
            year = 0

        if year and not year == 'None':
            year_now = datetime.datetime.now().strftime("%Y")
            if int(year_now) - int(year) >= settings.TELEMETA_PUBLIC_ACCESS_PERIOD:
                access = 'full'

    return access


def get_revisions(nb, user=None):
    last_revisions = Revision.objects.order_by('-time')
    if user:
        last_revisions = last_revisions.filter(user=user)
    last_revisions = last_revisions[0:nb]
    revisions = []

    for revision in last_revisions:
        for type in mods.keys():
            if revision.element_type == type:
                try:
                    element = mods[type].objects.get(pk=revision.element_id)
                except:
                    element = None
        if not element == None:
            revisions.append({'revision': revision, 'element': element})
    return revisions


def get_playlists(request, user=None):
    if not user:
        user = request.user
    playlists = []
    if user.is_authenticated():
        user_playlists = Playlist.objects.filter(author=user)
        for playlist in user_playlists:
            playlist_resources = PlaylistResource.objects.filter(playlist=playlist)
            resources = []
            for resource in playlist_resources:
                try:
                    for type in mods.keys():
                        if resource.resource_type == type:
                            element = mods[type].objects.get(id=resource.resource_id)
                except:
                    element = None
                resources.append({'element': element, 'type': resource.resource_type, 'public_id': resource.public_id})
            playlists.append({'playlist': playlist, 'resources': resources})
        # add by Killian Mary for sort playlist by title
        playlists.sort(key=lambda x: x['playlist'].title)
    return playlists


def get_playlists_names(request, user=None):
    if not user:
        user = request.user
    playlists = []
    if user.is_authenticated():
        user_playlists = user.playlists.all()
        for playlist in user_playlists:
            playlists.append({'playlist': playlist})
    return playlists


def check_related_media(medias):
    for media in medias:
        if not media.mime_type:
            media.set_mime_type()
            media.save()
        if not media.title and media.url:
            if 'https' in media.url:
                media.url = media.url.replace('https', 'http')
            import lxml.etree
            parser = lxml.etree.HTMLParser()
            tree = lxml.etree.parse(media.url, parser)
            try:
                title = tree.find(".//title").text
            except:
                title = media.url
            media.title = title.replace('\n', '').strip()
            media.save()


def auto_code(collection):
    items = collection.items.all()
    suffixes = []

    if items:
        for item in items:
            if '_' in item.public_id:
                try:
                    split = item.public_id.split('_')
                    suffix = int(split[-1])
                    prefix = split[:-1]
                except:
                    suffix = 999

                suffixes.append(suffix)

    if suffixes:
        return collection.code + '_' + str(max(suffixes) + 1)
    else:
        return collection.code + '_001'


def get_room(content_type=None, id=None, name=None):
    rooms = jqchat.models.Room.objects.filter(content_type=content_type,
                                              object_id=id)
    if not rooms:
        room = jqchat.models.Room.objects.create(content_type=content_type,
                                                 object_id=id,
                                                 name=name[:254])
    else:
        room = rooms[0]
    return room


def get_kwargs_or_none(key, kwargs):
    if key in kwargs.keys():
        return kwargs[key]
    else:
        return None


def cleanup_path(path):
    new_path = []
    for dir in path.split(os.sep):
        new_path.append(slugify(dir))
    return os.sep.join(new_path)

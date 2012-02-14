# -*- coding: utf-8 -*-
# Copyright (C) 2007-2010 Samalyse SARL
# Copyright (C) 2010-2012 Parisson SARL

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

# Authors: Olivier Guilyardi <olivier@samalyse.com>
#          Guillaume Pellerin <yomguy@parisson.com>

import re
import os
import sys
import csv
import time
import random
import datetime
import timeside

from jsonrpc import jsonrpc_method

from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate, login
from django.template import RequestContext, loader
from django import template
from django.http import HttpResponse, HttpResponseRedirect
from django.http import Http404
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.views.generic import list_detail
from django.views.generic import DetailView
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

from telemeta.models import *
import telemeta.models
import telemeta.interop.oai as oai
from telemeta.interop.oaidatasource import TelemetaOAIDataSource
from telemeta.util.unaccent import unaccent
from telemeta.util.unaccent import unaccent_icmp
from telemeta.util.logger import Logger
from telemeta.util.unicode import UnicodeWriter
from telemeta.cache import TelemetaCache
import telemeta.views.pages as pages
from telemeta.forms import *

# Model type definition
mods = {'item': MediaItem, 'collection': MediaCollection,
        'corpus': MediaCorpus, 'fonds': MediaFonds, 'marker': MediaItemMarker, }

# TOOLS

def render(request, template, data = None, mimetype = None):
    return render_to_response(template, data, context_instance=RequestContext(request),
                              mimetype=mimetype)

def stream_from_processor(__decoder, __processor, __flag, metadata=None):
    while True:
        __frames, __eodproc = __processor.process(*__decoder.process())
        if __eodproc or not len(__frames):
            if metadata:
                __processor.set_metadata(metadata)
                __processor.write_metadata()
            __flag.value = True
            __flag.save()
            break
        yield __processor.chunk

def stream_from_file(__file):
    chunk_size = 0x10000
    f = open(__file, 'r')
    while True:
        __chunk = f.read(chunk_size)
        if not len(__chunk):
            f.close()
            break
        yield __chunk

def get_public_access(access, year_from=None, year_to=None):
    # Rolling publishing date : public access is given when time between recorded year
    # and current year is over the settings value PUBLIC_ACCESS_PERIOD
    if year_from and not year_from == 0:
        year = year_from
    elif year_to and not year_to == 0:
        year = year_to
    else:
        year = 0
    if access == 'full':
        public_access = True
    else:
        public_access = False
        if year and not year == 'None':
            year_now = datetime.datetime.now().strftime("%Y")
            if int(year_now) - int(year) >= settings.TELEMETA_PUBLIC_ACCESS_PERIOD:
                public_access = True
        else:
            public_access = False
    return public_access

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
                resources.append({'element': element, 'type': resource.resource_type, 'public_id': resource.public_id })
            playlists.append({'playlist': playlist, 'resources': resources})
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
            title = tree.find(".//title").text
            media.title = title.replace('\n', '').strip()
            media.save()

def auto_code(resources, base_code):
    index = 1
    while True:
        code = base_code + '_' + str(index)
        r = resources.filter(code=code)
        if not r:
            break
        index += 1
    return code


class GeneralView(object):
    """Provide general web UI methods"""

    def home(self, request):
        """Render the index page"""

        template = loader.get_template('telemeta/home.html')

        sound_items = MediaItem.objects.sound()
        _sound_pub_items = []
        for item in sound_items:
            if get_public_access(item.public_access,  str(item.recorded_from_date).split('-')[0],
                                            str(item.recorded_to_date).split('-')[0]):
                _sound_pub_items.append(item)

        random.shuffle(_sound_pub_items)
        if len(_sound_pub_items) != 0:
            sound_pub_item = _sound_pub_items[0]
        else:
            sound_pub_item = None
        if len(_sound_pub_items) == 2:
            sound_pub_items = [_sound_pub_items[1]]
        elif len(_sound_pub_items) > 2:
            sound_pub_items = _sound_pub_items[1:3]
        else:
            sound_pub_items = None

        revisions = get_revisions(4)
        context = RequestContext(request, {
                    'page_content': pages.get_page_content(request, 'home', ignore_slash_issue=True),
                    'revisions': revisions,  'sound_pub_items': sound_pub_items,
                    'sound_pub_item': sound_pub_item })
        return HttpResponse(template.render(context))

    def lists(self, request):
        """Render the home page"""

        if request.user.is_authenticated():
            template='telemeta/lists.html'
            playlists = get_playlists(request)
            revisions = get_revisions(100)
            searches = Search.objects.filter(username=request.user)
            user_revisions = get_revisions(25, request.user)
            return render(request, template, {'playlists': playlists, 'searches': searches,
                                              'revisions': revisions, 'user_revisions': user_revisions })
        else:
            template = 'telemeta/messages.html'
            mess = ugettext('Access not allowed')
            title = ugettext('Lists') + ' : ' + mess
            description = ugettext('Please login or contact the website administator to get a private access.')
            messages.error(request, title)
            return render(request, template, {'description' : description})

    def edit_search(self, request, criteria=None):
        year_min, year_max = MediaCollection.objects.all().recording_year_range()
        rec_years = year_min and year_max and range(year_min, year_max + 1) or []
        year_min, year_max = MediaCollection.objects.all().publishing_year_range()
        pub_years = year_min and year_max and range(year_min, year_max + 1) or []
        return render(request, 'telemeta/search_criteria.html', {
            'rec_years': rec_years,
            'pub_years': pub_years,
            'ethnic_groups': MediaItem.objects.all().ethnic_groups(),
            'criteria': criteria
        })

    def handle_oai_request(self, request):
        host = request.META['HTTP_HOST']
        datasource  = TelemetaOAIDataSource()
        repository_name = settings.TELEMETA_ORGANIZATION
        url         = 'http://' + host + request.path
        admin       = settings.ADMINS[0][1]
        provider    = oai.DataProvider(datasource, repository_name, url, admin)
        args        = request.GET.copy()
        args.update(request.POST)
        return HttpResponse(provider.handle(args), mimetype='text/xml')

    def render_flatpage(self, request, path):
        try:
            content = pages.get_page_content(request, path)
        except pages.MalformedPagePath:
            return redirect(request.path + '/')

        if isinstance(content, pages.PageAttachment):
            return HttpResponse(content, content.mimetype())
        else:
            return render(request, 'telemeta/flatpage.html', {'page_content': content })

    def logout(self, request):
        auth.logout(request)
        return redirect('telemeta-home')

    def search(self, request, type = None):
        """Perform a search through collections and items metadata"""
        collections = MediaCollection.objects.enriched()
        items = MediaItem.objects.enriched()
        corpus = MediaCorpus.objects.all()
        fonds  = MediaFonds.objects.all()
        input = request.REQUEST
        criteria = {}

        switch = {
            'pattern': lambda value: (
                collections.quick_search(value),
                items.quick_search(value),
                corpus.quick_search(value),
                fonds.quick_search(value),
                ),
            'title': lambda value: (
                collections.word_search('title', value),
                items.by_title(value),
                corpus.word_search('title', value),
                fonds.word_search('title', value)),
            'location': lambda value: (
                collections.by_location(Location.objects.get(name=value)),
                items.by_location(Location.objects.get(name=value))),
            'continent': lambda value: (
                collections.by_continent(value),
                items.filter(continent = value)),
            'ethnic_group': lambda value: (
                collections.by_ethnic_group(value),
                items.filter(ethnic_group = value),
                EthnicGroup.objects.get(pk=value)),
            'creator': lambda value: (
                collections.word_search('creator', value),
                items.word_search('collection__creator', value)),
            'collector': lambda value: (
                collections.by_fuzzy_collector(value),
                items.by_fuzzy_collector(value)),
            'rec_year_from': lambda value: (
                collections.by_recording_year(int(value), int(input.get('rec_year_to', value))),
                items.by_recording_date(datetime.date(int(value), 1, 1),
                                        datetime.date(int(input.get('rec_year_to', value)), 12, 31))),
            'rec_year_to': lambda value: (collections, items),
            'pub_year_from': lambda value: (
                collections.by_publish_year(int(value), int(input.get('pub_year_to', value))),
                items.by_publish_year(int(value), int(input.get('pub_year_to', value)))),
            'pub_year_to': lambda value: (collections, items),
            'sound': lambda value: (
                collections.sound(),
                items.sound()),
        }

        for key, value in input.items():
            func = switch.get(key)
            if func and value and value != "0":
                try:
                    res = func(value)
                    if len(res)  > 4:
                        collections, items, corpus, fonds, value = res
                    elif len(res) == 4:
                        collections, items, corpus, fonds = res
                    elif len(res) == 3:
                        collections, items, value = res
                        corpus = corpus.none()
                        fonds = fonds.none()
                    else:
                        collections, items = res
                        corpus = corpus.none()
                        fonds = fonds.none()

                except ObjectDoesNotExist:
                    collections = collections.none()
                    items = items.none()
                    corpus = corpus.none()
                    fonds = fonds.none()

                criteria[key] = value

        # Save the search
        user = request.user
        if user:
            if user.is_authenticated():
                search = Search(username=user)
                search.save()
                if criteria:
                    for key in criteria.keys():
                        value = criteria[key]
                        if key == 'ethnic_group':
                            try:
                                group = EthnicGroup.objects.get(value=value)
                                value = group.id
                            except:
                                value = ''
                        criter = Criteria(key=key, value=value)
                        criter.save()
                        search.criteria.add(criter)
                    search.save()

        if type is None:
            if items.count():
                type = 'items'
            else:
                type = 'collections'

        if type == 'items':
            objects = items
        elif type == 'collections':
            objects = collections
        elif type == 'corpus':
            objects = corpus
        elif type == 'fonds':
            objects = fonds

        return list_detail.object_list(request, objects,
            template_name='telemeta/search_results.html', paginate_by=20,
            extra_context={'criteria': criteria, 'collections_num': collections.count(),
                'items_num': items.count(), 'corpus_num': corpus.count(), 'fonds_num': fonds.count(),
                'type' : type,})

    def complete_location(self, request, with_items=True):
        input = request.REQUEST

        token = input['q']
        limit = int(input['limit'])
        if with_items:
            locations = MediaItem.objects.all().locations()
        else:
            locations = Location.objects.all()

        locations = locations.filter(name__istartswith=token).order_by('name')[:limit]
        data = [unicode(l) + " (%d items)" % l.items().count() for l in locations]

        return HttpResponse("\n".join(data))

    def users(self, request):
        users = User.objects.all()
        return render(request, 'telemeta/users.html', {'users': users})

class CollectionView(object):
    """Provide Collections web UI methods"""

    def collection_detail(self, request, public_id, template='telemeta/collection_detail.html'):
        collection = MediaCollection.objects.get(public_id=public_id)
        items = collection.items.enriched()
        items = items.order_by('code', 'old_code')

        if collection.public_access == 'none' and not (request.user.is_staff or request.user.is_superuser):
            mess = ugettext('Access not allowed')
            title = ugettext('Collection') + ' : ' + public_id + ' : ' + mess
            description = ugettext('Please login or contact the website administator to get a private access.')
            messages.error(request, title)
            return render(request, 'telemeta/messages.html', {'description' : description})

        public_access = get_public_access(collection.public_access, collection.recorded_from_year,
                                                collection.recorded_to_year)
        playlists = get_playlists(request)

        related_media = MediaCollectionRelated.objects.filter(collection=collection)
        check_related_media(related_media)
        parents = MediaCorpus.objects.filter(children=collection)

        return render(request, template, {'collection': collection, 'playlists': playlists, 'public_access': public_access, 'items': items, 'related_media': related_media, 'parents': parents })

    @method_decorator(permission_required('telemeta.change_mediacollection'))
    def collection_edit(self, request, public_id, template='telemeta/collection_edit.html'):
        collection = MediaCollection.objects.get(public_id=public_id)
        if request.method == 'POST':
            form = MediaCollectionForm(data=request.POST, files=request.FILES, instance=collection)
            if form.is_valid():
                code = form.cleaned_data['code']
                if not code:
                    code = public_id
                form.save()
                collection.set_revision(request.user)
                return HttpResponseRedirect('/archives/collections/'+code)
        else:
            form = MediaCollectionForm(instance=collection)

        return render(request, template, {'collection': collection, "form": form,})

    @method_decorator(permission_required('telemeta.add_mediacollection'))
    def collection_add(self, request, template='telemeta/collection_add.html'):
        collection = MediaCollection()
        if request.method == 'POST':
            form = MediaCollectionForm(data=request.POST, files=request.FILES, instance=collection)
            if form.is_valid():
                code = form.cleaned_data['code']
                if not code:
                    code = public_id
                form.save()
                collection.set_revision(request.user)
                return HttpResponseRedirect('/archives/collections/'+code)
        else:
            form = MediaCollectionForm(instance=collection)

        return render(request, template, {'collection': collection, "form": form,})

    @method_decorator(permission_required('telemeta.add_mediacollection'))
    def collection_copy(self, request, public_id, template='telemeta/collection_edit.html'):
        if request.method == 'POST':
            collection = MediaCollection()
            form = MediaCollectionForm(data=request.POST, files=request.FILES, instance=collection)
            if form.is_valid():
                code = form.cleaned_data['code']
                if not code:
                    code = public_id
                form.save()
                collection.set_revision(request.user)
                return HttpResponseRedirect('/archives/collections/'+code)
        else:
            collection = MediaCollection.objects.get(public_id=public_id)
            form = MediaCollectionForm(instance=collection)

        return render(request, template, {'collection': collection, "form": form,})

    def collection_playlist(self, request, public_id, template, mimetype):
        try:
            collection = MediaCollection.objects.get(public_id=public_id)
        except ObjectDoesNotExist:
            raise Http404

        template = loader.get_template(template)
        context = RequestContext(request, {'collection': collection, 'host': request.META['HTTP_HOST']})
        return HttpResponse(template.render(context), mimetype=mimetype)

    @method_decorator(permission_required('telemeta.delete_mediacollection'))
    def collection_delete(self, request, public_id):
        """Delete a given collection"""
        collection = MediaCollection.objects.get(public_id=public_id)
        collection.delete()
        return HttpResponseRedirect('/archives/collections/')

    def related_media_collection_stream(self, request, collection_public_id, media_id):
        collection = MediaCollection.objects.get(public_id=collection_public_id)
        media = MediaCollectionRelated.objects.get(collection=collection, id=media_id)
        response = HttpResponse(stream_from_file(media.file.path), mimetype=media.mime_type)
#        response['Content-Disposition'] = 'attachment'
        return response

    @method_decorator(permission_required('telemeta.change_mediacollection'))
    def related_media_edit(self, request, public_id, template):
        collection = MediaCollection.objects.get(public_id=public_id)
        MediaCollectionRelatedFormSet = inlineformset_factory(MediaCollection, MediaCollectionRelated, form=MediaCollectionRelatedForm)
        if request.method == 'POST':
            formset = MediaCollectionRelatedFormSet(data=request.POST, files=request.FILES, instance=collection)
            if formset.is_valid():
                formset.save()
                collection.set_revision(request.user)
                return HttpResponseRedirect('/archives/collections/'+public_id)
        else:
            formset = MediaCollectionRelatedFormSet(instance=collection)

        return render(request, template, {'collection': collection, 'formset': formset,})

class ItemView(object):
    """Provide Collections web UI methods"""

    graphers = timeside.core.processors(timeside.api.IGrapher)
    decoders = timeside.core.processors(timeside.api.IDecoder)
    encoders = timeside.core.processors(timeside.api.IEncoder)
    analyzers = timeside.core.processors(timeside.api.IAnalyzer)
    cache_data = TelemetaCache(settings.TELEMETA_DATA_CACHE_DIR)
    cache_export = TelemetaCache(settings.TELEMETA_EXPORT_CACHE_DIR)

    def item_previous_next(self, item):
        # Get previous and next items
        pks = []
        items = MediaItem.objects.filter(collection=item.collection)
        items = items.order_by('code', 'old_code')

        if len(items) > 1:
            for it in items:
                pks.append(it.pk)
            for pk in pks:
                if pk == item.pk:
                    if pk == pks[0]:
                        previous_pk = pks[-1]
                        next_pk = pks[1]
                    elif pk == pks[-1]:
                        previous_pk = pks[-2]
                        next_pk = pks[0]
                    else:
                        previous_pk = pks[pks.index(pk)-1]
                        next_pk = pks[pks.index(pk)+1]
                    for it in items:
                        if it.pk == previous_pk:
                            previous = it
                        if it.pk == next_pk:
                            next = it
                    previous = previous.public_id
                    next = next.public_id
        else:
             previous = item.public_id
             next = item.public_id

        return previous, next

    def item_detail(self, request, public_id=None, marker_id=None, width=None, height=None,
                        template='telemeta/mediaitem_detail.html'):
        """Show the details of a given item"""

        if not public_id and marker_id:
            marker = MediaItemMarker.objects.get(public_id=marker_id)
            item_id = marker.item_id
            item = MediaItem.objects.get(id=item_id)
        else:
            item = MediaItem.objects.get(public_id=public_id)

        item_public_access = item.public_access != 'none' or item.collection.public_access != 'none'
        if not item_public_access and not (request.user.is_staff or request.user.is_superuser):
            mess = ugettext('Access not allowed')
            title = ugettext('Item') + ' : ' + public_id + ' : ' + mess
            description = ugettext('Please login or contact the website administator to get a private access.')
            messages.error(request, title)
            return render(request, 'telemeta/messages.html', {'description' : description})

        # Get TimeSide processors
        formats = []
        for encoder in self.encoders:
            if settings.TELEMETA_DOWNLOAD_FORMATS:
                if encoder.file_extension() in settings.TELEMETA_DOWNLOAD_FORMATS:
                    formats.append({'name': encoder.format(), 'extension': encoder.file_extension()})
            else:
                formats.append({'name': encoder.format(), 'extension': encoder.file_extension()})

        graphers = []
        for grapher in self.graphers:
            graphers.append({'name':grapher.name(), 'id': grapher.id()})
        if request.REQUEST.has_key('grapher_id'):
            grapher_id = request.REQUEST['grapher_id']
        else:
            grapher_id = 'waveform'

        previous, next = self.item_previous_next(item)
        mime_type = self.item_analyze(item)
        playlists = get_playlists(request)
        public_access = get_public_access(item.public_access, str(item.recorded_from_date).split('-')[0],
                                                str(item.recorded_to_date).split('-')[0])

        related_media = MediaItemRelated.objects.filter(item=item)
        check_related_media(related_media)

        return render(request, template,
                    {'item': item, 'export_formats': formats,
                    'visualizers': graphers, 'visualizer_id': grapher_id,
                    'audio_export_enabled': getattr(settings, 'TELEMETA_DOWNLOAD_ENABLED', True),
                    'previous' : previous, 'next' : next, 'marker': marker_id, 'playlists' : playlists,
                    'public_access': public_access, 'width': width, 'height': height,
                    'related_media': related_media, 'mime_type': mime_type,
                    })

    @method_decorator(permission_required('telemeta.change_mediaitem'))
    def item_edit(self, request, public_id, template='telemeta/mediaitem_edit.html'):
        """Edit a given item"""
        item = MediaItem.objects.get(public_id=public_id)

        formats = []
        for encoder in self.encoders:
            #FIXME: timeside cannot encode to FLAC and OGG now :'(
            if encoder.file_extension() != 'ogg' and encoder.file_extension() != 'flac':
                formats.append({'name': encoder.format(), 'extension': encoder.file_extension()})

        graphers = []
        for grapher in self.graphers:
            graphers.append({'name':grapher.name(), 'id': grapher.id()})
        if request.REQUEST.has_key('grapher_id'):
            grapher_id = request.REQUEST['grapher_id']
        else:
            grapher_id = 'waveform'

        previous, next = self.item_previous_next(item)
        mime_type = self.item_analyze(item)

        if request.method == 'POST':
            form = MediaItemForm(data=request.POST, files=request.FILES, instance=item)
            if form.is_valid():
                form.save()
                code = form.cleaned_data['code']
                if not code:
                    code = str(item.id)
                if form.files:
                    self.cache_data.delete_item_data(code)
                    self.cache_export.delete_item_data(code)
                    flags = MediaItemTranscodingFlag.objects.filter(item=item)
                    analyses = MediaItemAnalysis.objects.filter(item=item)
                    for flag in flags:
                        flag.delete()
                    for analysis in analyses:
                        analysis.delete()
                item.set_revision(request.user)
                return HttpResponseRedirect('/archives/items/'+code)
        else:
            form = MediaItemForm(instance=item)

        return render(request, template,
                    {'item': item, 'export_formats': formats,
                    'visualizers': graphers, 'visualizer_id': grapher_id,
                    'audio_export_enabled': getattr(settings, 'TELEMETA_DOWNLOAD_ENABLED', True), "form": form,
                    'previous' : previous, 'next' : next, 'mime_type': mime_type,
                    })

    def related_media_item_stream(self, request, item_public_id, media_id):
        item = MediaItem.objects.get(public_id=item_public_id)
        media = MediaItemRelated.objects.get(item=item, id=media_id)
        response = HttpResponse(stream_from_file(media.file.path), mimetype=media.mime_type)
#        response['Content-Disposition'] = 'attachment; '+'filename='+media.title+'.'+ext
        return response

    @method_decorator(permission_required('telemeta.change_mediaitem'))
    def related_media_edit(self, request, public_id, template):
        item = MediaItem.objects.get(public_id=public_id)
        MediaItemRelatedFormSet = inlineformset_factory(MediaItem, MediaItemRelated, form=MediaItemRelatedForm)
        if request.method == 'POST':
            formset = MediaItemRelatedFormSet(data=request.POST, files=request.FILES, instance=item)
            if formset.is_valid():
                formset.save()
                item.set_revision(request.user)
                return HttpResponseRedirect('/archives/items/'+public_id)
        else:
            formset = MediaItemRelatedFormSet(instance=item)

        return render(request, template, {'item': item, 'formset': formset,})

    @method_decorator(permission_required('telemeta.add_mediaitem'))
    def item_add(self, request, public_id=None, template='telemeta/mediaitem_add.html'):
        """Add an item"""
        if public_id:
            collection = MediaCollection.objects.get(public_id=public_id)
            items = MediaItem.objects.filter(collection=collection)
            code = auto_code(items, collection.code)
            item = MediaItem(collection=collection, code=code)
        else:
            item = MediaItem()
        if request.method == 'POST':
            form = MediaItemForm(data=request.POST, files=request.FILES, instance=item)
            if form.is_valid():
                form.save()
                item.set_revision(request.user)
                code = form.cleaned_data['code']
                if not code:
                    code = str(item.id)
                return HttpResponseRedirect('/archives/items/'+code)
        else:
            form = MediaItemForm(instance=item)


        return render(request, template, {'item': item, 'form': form})

    @method_decorator(permission_required('telemeta.add_mediaitem'))
    def item_copy(self, request, public_id, template='telemeta/mediaitem_copy.html'):
        """Copy a given item"""
        if request.method == 'POST':
            source_item = MediaItem.objects.get(public_id=public_id)
            item = MediaItem()
            form = MediaItemForm(data=request.POST, files=request.FILES, instance=item)
            if form.is_valid():
                form.save()
                code = form.cleaned_data['code']
                if not code:
                    code = str(item.id)

                performances = MediaItemPerformance.objects.filter(media_item=source_item)
                for performance in performances:
                    performance.pk = None
                    performance.id = None
                    performance.media_item = item
                    performance.save()

                keywords = MediaItemKeyword.objects.filter(item=source_item)
                for keyword in keywords:
                    keyword.pk = None
                    keyword.id = None
                    keyword.item = item
                    keyword.save()

                item.set_revision(request.user)
                return HttpResponseRedirect('/archives/items/'+code)
        else:
            item = MediaItem.objects.get(public_id=public_id)
            items = MediaItem.objects.filter(collection=item.collection)
            item.code = auto_code(items, item.collection.code)
            item.approx_duration = ''
            form = MediaItemForm(instance=item)
            form.code = item.code
            form.file = None

        return render(request, template, {'item': item, "form": form})

    @method_decorator(permission_required('telemeta.delete_mediaitem'))
    def item_delete(self, request, public_id):
        """Delete a given item"""
        item = MediaItem.objects.get(public_id=public_id)
        collection = item.collection
        item.delete()
        return HttpResponseRedirect('/archives/collections/'+collection.code)

    def item_analyze(self, item):
        analyses = MediaItemAnalysis.objects.filter(item=item)
        mime_type = ''

        if analyses:
            for analysis in analyses:
                if not item.approx_duration and analysis.analyzer_id == 'duration':
                    value = analysis.value
                    time = value.split(':')
                    time[2] = time[2].split('.')[0]
                    time = ':'.join(time)
                    item.approx_duration = time
                    item.save()
                if analysis.analyzer_id == 'mime_type':
                    mime_type = analysis.value
        else:
            analyzers = []
            analyzers_sub = []
            if item.file:
                decoder  = timeside.decoder.FileDecoder(item.file.path)
                pipe = decoder
                for analyzer in self.analyzers:
                    subpipe = analyzer()
                    analyzers_sub.append(subpipe)
                    pipe = pipe | subpipe
                pipe.run()

                mime_type = decoder.format()
                analysis = MediaItemAnalysis(item=item, name='MIME type',
                                             analyzer_id='mime_type', unit='', value=mime_type)
                analysis.save()
                analysis = MediaItemAnalysis(item=item, name='Channels',
                                             analyzer_id='channels',
                                             unit='', value=decoder.channels())
                analysis.save()
                analysis = MediaItemAnalysis(item=item, name='Samplerate',
                                             analyzer_id='samplerate', unit='Hz',
                                             value=unicode(decoder.audiorate))
                analysis.save()
                analysis = MediaItemAnalysis(item=item, name='Resolution',
                                             analyzer_id='resolution', unit='bits',
                                             value=unicode(decoder.audiowidth))
                analysis.save()
                analysis = MediaItemAnalysis(item=item, name='Duration',
                                             analyzer_id='duration', unit='s',
                                             value=unicode(datetime.timedelta(0,decoder.duration)))
                analysis.save()

                for analyzer in analyzers_sub:
                    value = analyzer.result()
                    analysis = MediaItemAnalysis(item=item, name=analyzer.name(),
                                                 analyzer_id=analyzer.id(),
                                                 unit=analyzer.unit(), value=str(value))
                    analysis.save()

#                FIXME: parse tags on first load
#                tags = decoder.tags

        return mime_type

    def item_analyze_xml(self, request, public_id):
        item = MediaItem.objects.get(public_id=public_id)
        analyses = MediaItemAnalysis.objects.filter(item=item)
        analyzers = []
        for analysis in analyses:
            analyzers.append(analysis.to_dict())
        mime_type = 'text/xml'
        response = HttpResponse(self.cache_data.get_analyzer_xml(analyzers), mimetype=mime_type)
        response['Content-Disposition'] = 'attachment; filename='+public_id+'.xml'
        return response

    def item_visualize(self, request, public_id, visualizer_id, width, height):
        item = MediaItem.objects.get(public_id=public_id)
        mime_type = 'image/png'
        grapher_id = visualizer_id

        for grapher in self.graphers:
            if grapher.id() == grapher_id:
                break

        if grapher.id() != grapher_id:
            raise Http404

        size = width + '_' + height
        image_file = '.'.join([public_id, grapher_id, size, 'png'])

        if not self.cache_data.exists(image_file):
            if item.file:
                path = self.cache_data.dir + os.sep + image_file
                decoder  = timeside.decoder.FileDecoder(item.file.path)
                graph = grapher(width = int(width), height = int(height))
                pipe = decoder | graph
                pipe.run()
                graph.watermark('timeside', opacity=.6, margin=(5,5))
                f = open(path, 'w')
                graph.render(path)
                f.close()

        response = HttpResponse(self.cache_data.read_stream_bin(image_file), mimetype=mime_type)
        return response

    def list_export_extensions(self):
        "Return the recognized item export file extensions, as a list"
        list = []
        for encoder in self.encoders:
            list.append(encoder.file_extension())
        return list

    def item_export(self, request, public_id, extension):
        """Export a given media item in the specified format (OGG, FLAC, ...)"""

        item = MediaItem.objects.get(public_id=public_id)
        public_access = get_public_access(item.public_access,
                                          str(item.recorded_from_date).split('-')[0],
                                          str(item.recorded_to_date).split('-')[0])

        if (not public_access or not extension in settings.TELEMETA_STREAMING_FORMATS) and \
                    not (request.user.has_perm('telemeta.can_play_all_items') or request.user.is_superuser):
            mess = ugettext('Access not allowed')
            title = 'Item file : ' + public_id + '.' + extension + ' : ' + mess
            description = ugettext('Please login or contact the website administator to get a private access.')
            messages.error(request, title)
            return render(request, 'telemeta/messages.html', {'description' : description})

        for encoder in self.encoders:
            if encoder.file_extension() == extension:
                break

        if encoder.file_extension() != extension:
            raise Http404('Unknown export file extension: %s' % extension)

        mime_type = encoder.mime_type()
        file = public_id + '.' + encoder.file_extension()
        audio = item.file.path

        flag = MediaItemTranscodingFlag.objects.filter(item=item, mime_type=mime_type)
        if not flag:
            flag = MediaItemTranscodingFlag(item=item, mime_type=mime_type)
            flag.value = False
            flag.save()
        else:
            flag = flag[0]

        format = self.item_analyze(item)
        dc_metadata = dublincore.express_item(item).to_list()
        mapping = DublinCoreToFormatMetadata(extension)
        metadata = mapping.get_metadata(dc_metadata)

        if mime_type in format:
            # source > stream
            if not extension in mapping.unavailable_extensions:
                proc = encoder(audio)
                proc.set_metadata(metadata)
                try:
                    proc.write_metadata()
                except:
                    pass
            response = HttpResponse(stream_from_file(audio), mimetype = mime_type)
        else:
            media = self.cache_export.dir + os.sep + file
            if not self.cache_export.exists(file) or not flag.value:
                # source > encoder > stream
                decoder = timeside.decoder.FileDecoder(audio)
                decoder.setup()
                proc = encoder(media, streaming=True)
                proc.setup(channels=decoder.channels(), samplerate=decoder.samplerate())
                if extension in mapping.unavailable_extensions:
                    metadata=None
                response = HttpResponse(stream_from_processor(decoder, proc, flag, metadata=metadata), mimetype = mime_type)
            else:
                # cache > stream
                response = HttpResponse(self.cache_export.read_stream_bin(file), mimetype = mime_type)

        response['Content-Disposition'] = 'attachment'
        return response

    def item_playlist(self, request, public_id, template, mimetype):
        try:
            item = MediaItem.objects.get(public_id=public_id)
        except ObjectDoesNotExist:
            raise Http404

        template = loader.get_template(template)
        context = RequestContext(request, {'item': item, 'host': request.META['HTTP_HOST']})
        return HttpResponse(template.render(context), mimetype=mimetype)

    @method_decorator(permission_required('telemeta.change_mediaitem'))
    def item_performances_edit(self, request, public_id, template):
        item = MediaItem.objects.get(public_id=public_id)
        PerformanceFormSet = inlineformset_factory(MediaItem, MediaItemPerformance, form=MediaItemPerformanceForm)
        if request.method == 'POST':
            formset = PerformanceFormSet(data=request.POST, instance=item)
            if formset.is_valid():
                formset.save()
                return HttpResponseRedirect('/archives/items/'+public_id)
        else:
            formset = PerformanceFormSet(instance=item)
        return render(request, template, {'item': item, 'formset': formset,})

    @method_decorator(permission_required('telemeta.change_mediaitem'))
    def item_keywords_edit(self, request, public_id, template):
        item = MediaItem.objects.get(public_id=public_id)
        FormSet = inlineformset_factory(MediaItem, MediaItemKeyword)
        if request.method == 'POST':
            formset = FormSet(data=request.POST, instance=item)
            if formset.is_valid():
                formset.save()
                return HttpResponseRedirect('/archives/items/'+public_id)
        else:
            formset = FormSet(instance=item)
        return render(request, template, {'item': item, 'formset': formset,})


class AdminView(object):
    """Provide Admin web UI methods"""

    @method_decorator(permission_required('sites.change_site'))
    def admin_index(self, request):
        return render(request, 'telemeta/admin.html', self.__get_admin_context_vars())

    @method_decorator(permission_required('sites.change_site'))
    def admin_general(self, request):
        return render(request, 'telemeta/admin_general.html', self.__get_admin_context_vars())

    @method_decorator(permission_required('sites.change_site'))
    def admin_enumerations(self, request):
        return render(request, 'telemeta/admin_enumerations.html', self.__get_admin_context_vars())

    @method_decorator(permission_required('sites.change_site'))
    def admin_users(self, request):
        users = User.objects.all()
        return render(request, 'telemeta/admin_users.html', {'users': users})

    def __get_enumerations_list(self):
        from django.db.models import get_models
        models = get_models(telemeta.models)

        enumerations = []
        for model in models:
            if issubclass(model, Enumeration):
                enumerations.append({"name": model._meta.verbose_name,
                    "id": model._meta.module_name})

        cmp = lambda obj1, obj2: unaccent_icmp(obj1['name'], obj2['name'])
        enumerations.sort(cmp)
        return enumerations

    def __get_admin_context_vars(self):
        return {"enumerations": self.__get_enumerations_list()}

    def __get_enumeration(self, id):
        from django.db.models import get_models
        models = get_models(telemeta.models)
        for model in models:
            if model._meta.module_name == id:
                break

        if model._meta.module_name != id:
            return None

        return model

    @method_decorator(permission_required('telemeta.change_keyword'))
    def edit_enumeration(self, request, enumeration_id):

        enumeration  = self.__get_enumeration(enumeration_id)
        if enumeration == None:
            raise Http404

        vars = self.__get_admin_context_vars()
        vars["enumeration_id"] = enumeration._meta.module_name
        vars["enumeration_name"] = enumeration._meta.verbose_name
        vars["enumeration_values"] = enumeration.objects.all()
        return render(request, 'telemeta/enumeration_edit.html', vars)

    @method_decorator(permission_required('telemeta.add_keyword'))
    def add_to_enumeration(self, request, enumeration_id):

        enumeration  = self.__get_enumeration(enumeration_id)
        if enumeration == None:
            raise Http404

        enumeration_value = enumeration(value=request.POST['value'])
        enumeration_value.save()

        return self.edit_enumeration(request, enumeration_id)

    @method_decorator(permission_required('telemeta.change_keyword'))
    def update_enumeration(self, request, enumeration_id):

        enumeration  = self.__get_enumeration(enumeration_id)
        if enumeration == None:
            raise Http404

        if request.method == 'POST':
            enumeration.objects.filter(id__in=request.POST.getlist('sel')).delete()

        return self.edit_enumeration(request, enumeration_id)

    @method_decorator(permission_required('telemeta.change_keyword'))
    def edit_enumeration_value(self, request, enumeration_id, value_id):

        enumeration  = self.__get_enumeration(enumeration_id)
        if enumeration == None:
            raise Http404

        vars = self.__get_admin_context_vars()
        vars["enumeration_id"] = enumeration._meta.module_name
        vars["enumeration_name"] = enumeration._meta.verbose_name
        vars["enumeration_record"] = enumeration.objects.get(id__exact=value_id)
        return render(request, 'telemeta/enumeration_edit_value.html', vars)

    @method_decorator(permission_required('telemeta.change_keyword'))
    def update_enumeration_value(self, request, enumeration_id, value_id):

        if request.method == 'POST':
            enumeration  = self.__get_enumeration(enumeration_id)
            if enumeration == None:
                raise Http404

            record = enumeration.objects.get(id__exact=value_id)
            record.value = request.POST["value"]
            record.save()

        return self.edit_enumeration(request, enumeration_id)


class InstrumentView(object):
    """Provide Instrument web UI methods"""

    @method_decorator(permission_required('telemeta.change_instrument'))
    def edit_instrument(self, request):

        instruments = Instrument.objects.all().order_by('name')
        if instruments == None:
            raise Http404
        return render(request, 'telemeta/instrument_edit.html', {'instruments': instruments})

    @method_decorator(permission_required('telemeta.add_instrument'))
    def add_to_instrument(self, request):

        if request.method == 'POST':
            instrument = Instrument(name=request.POST['value'])
            instrument.save()

        return self.edit_instrument(request)

    @method_decorator(permission_required('telemeta.change_instrument'))
    def update_instrument(self, request):

        if request.method == 'POST':
            Instrument.objects.filter(id__in=request.POST.getlist('sel')).delete()

        return self.edit_instrument(request)

    @method_decorator(permission_required('telemeta.change_instrument'))
    def edit_instrument_value(self, request, value_id):
        instrument = Instrument.objects.get(id__exact=value_id)

        return render(request, 'telemeta/instrument_edit_value.html', {'instrument': instrument})

    @method_decorator(permission_required('telemeta.change_instrument'))
    def update_instrument_value(self, request, value_id):

        if request.method == 'POST':
            instrument = Instrument.objects.get(id__exact=value_id)
            instrument.name = request.POST["value"]
            instrument.save()

        return self.edit_instrument(request)


class GeoView(object):
    """Provide Geo web UI methods"""

    def list_continents(self, request):
        continents = MediaItem.objects.all().countries(group_by_continent=True)
        return render(request, 'telemeta/geo_continents.html',
                    {'continents': continents, 'gmap_key': settings.TELEMETA_GMAP_KEY })

    def country_info(self, request, id):
        country = Location.objects.get(pk=id)
        return render(request, 'telemeta/country_info.html', {
            'country': country, 'continent': country.continents()[0]})

    def list_countries(self, request, continent):
        continent = Location.objects.by_flatname(continent)[0]
        countries = MediaItem.objects.by_location(continent).countries()

        return render(request, 'telemeta/geo_countries.html', {
            'continent': continent,
            'countries': countries
        })

    def list_country_collections(self, request, continent, country):
        continent = Location.objects.by_flatname(continent)[0]
        country = Location.objects.by_flatname(country)[0]
        objects = MediaCollection.objects.enriched().by_location(country)
        return list_detail.object_list(request, objects,
            template_name='telemeta/geo_country_collections.html', paginate_by=20,
            extra_context={'country': country, 'continent': continent})

    def list_country_items(self, request, continent, country):
        continent = Location.objects.by_flatname(continent)[0]
        country = Location.objects.by_flatname(country)[0]
        objects = MediaItem.objects.enriched().by_location(country)
        return list_detail.object_list(request, objects,
            template_name='telemeta/geo_country_items.html', paginate_by=20,
            extra_context={'country': country, 'continent': continent})

class MarkerView(object):
    """Provide Collections web UI methods"""

    @jsonrpc_method('telemeta.add_marker')
    def add_marker(request, marker):
        # marker must be a dict
        if isinstance(marker, dict):
            item_id = marker['item_id']
            item = MediaItem.objects.get(id=item_id)
            m = MediaItemMarker(item=item)
            m.public_id = marker['public_id']
            m.time = float(marker['time'])
            m.title = marker['title']
            m.description = marker['description']
            m.author = User.objects.get(username=marker['author'])
            m.save()
            m.set_revision(request.user)
        else:
            raise 'Error : Bad marker dictionnary'

    @jsonrpc_method('telemeta.del_marker')
    def del_marker(request, public_id):
        m = MediaItemMarker.objects.get(public_id=public_id)
        m.delete()

    @jsonrpc_method('telemeta.get_markers')
    def get_markers(request, item_id):
        item = MediaItem.objects.get(id=item_id)
        markers = MediaItemMarker.objects.filter(item=item)
        list = []
        for marker in markers:
            dict = {}
            dict['public_id'] = marker.public_id
            dict['time'] = str(marker.time)
            dict['title'] = marker.title
            dict['description'] = marker.description
            dict['author'] = marker.author.username
            list.append(dict)
        return list

    @jsonrpc_method('telemeta.update_marker')
    def update_marker(request, marker):
        if isinstance(marker, dict):
            m = MediaItemMarker.objects.get(public_id=marker['public_id'])
            m.time = float(marker['time'])
            m.title = marker['title']
            m.description = marker['description']
            m.save()
            m.set_revision(request.user)
        else:
            raise 'Error : Bad marker dictionnary'

    @jsonrpc_method('telemeta.get_marker_id')
    def get_marker_id(request, public_id):
        marker = MediaItemMarker.objects.get(public_id=public_id)
        return marker.id

class PlaylistView(object):
    """Provide Playlist web UI methods"""

    @jsonrpc_method('telemeta.add_playlist')
    def add_playlist(request, playlist):
        # playlist must be a dict
        if isinstance(playlist, dict):
            m = Playlist()
            m.public_id = playlist['public_id']
            m.title = playlist['title']
            m.description = playlist['description']
            m.author = request.user
            m.save()
        else:
            raise 'Error : Bad playlist dictionnary'

    @jsonrpc_method('telemeta.del_playlist')
    def del_playlist(request, public_id):
        m = Playlist.objects.get(public_id=public_id)
        m.delete()

    @jsonrpc_method('telemeta.update_playlist')
    def update_playlist(request, playlist):
        if isinstance(playlist, dict):
            m = Playlist.objects.get(public_id=playlist['public_id'])
            m.title = playlist['title']
            m.description = playlist['description']
            m.save()
        else:
            raise 'Error : Bad playlist dictionnary'

    @jsonrpc_method('telemeta.add_playlist_resource')
    def add_playlist_resource(request, playlist_id, playlist_resource):
        # playlist_resource must be a dict
        if isinstance(playlist_resource, dict):
            m = PlaylistResource()
            m.public_id = playlist_resource['public_id']
            m.playlist = Playlist.objects.get(public_id=playlist_id, author=request.user)
            m.resource_type = playlist_resource['resource_type']
            m.resource_id = playlist_resource['resource_id']
            m.save()
        else:
            raise 'Error : Bad playlist_resource dictionnary'

    @jsonrpc_method('telemeta.del_playlist_resource')
    def del_playlist_resource(request, public_id):
        m = PlaylistResource.objects.get(public_id=public_id)
        m.delete()


    def playlist_csv_export(self, request, public_id, resource_type):
        playlist = Playlist.objects.get(public_id=public_id, author=request.user)
        resources = PlaylistResource.objects.filter(playlist=playlist)
        response = HttpResponse(mimetype='text/csv')
        response['Content-Disposition'] = 'attachment; filename='+playlist.title+'_'+resource_type+'.csv'
        writer = UnicodeWriter(response)

        elements = []
        for resource in resources:
            if resource_type == 'items':
                if resource.resource_type == 'collection':
                    collection = MediaCollection.objects.get(id=resource.resource_id)
                    collection_items = MediaItem.objects.filter(collection=collection)
                    for item in collection_items:
                        elements.append(item)
                elif resource.resource_type == 'item':
                    item = MediaItem.objects.get(id=resource.resource_id)
                    elements.append(item)

            elif resource_type == 'collections':
                if resource.resource_type == 'collection':
                    collection = MediaCollection.objects.get(id=resource.resource_id)
                    elements.append(collection)

        if elements:
            element = elements[0].to_dict()
            tags = element.keys()
            # code and title on the two first column
            tags.remove('code')
            tags.remove('title')
            tags.sort()
            tags.insert(0, 'title')
            tags.insert(0, 'code')
            writer.writerow(tags)

            for element in elements:
                data = []
                element = element.to_dict()
                for tag in tags:
                    data.append(element[tag])
                writer.writerow(data)
        return response


class ProfileView(object):
    """Provide Collections web UI methods"""

    @method_decorator(login_required)
    def profile_detail(self, request, username, template='telemeta/profile_detail.html'):
        user = User.objects.get(username=username)
        try:
            profile = user.get_profile()
        except:
            profile = None
        playlists = get_playlists(request, user)
        return render(request, template, {'profile' : profile, 'usr': user, 'playlists': playlists})

    def profile_edit(self, request, username, template='telemeta/profile_edit.html'):
        if request.user.is_superuser:
            user_hidden_fields = ['profile-user', 'user-password', 'user-last_login', 'user-date_joined']
        else:
            user_hidden_fields = ['user-username', 'user-is_staff', 'profile-user', 'user-is_active',
                         'user-password', 'user-last_login', 'user-date_joined', 'user-groups',
                         'user-user_permissions', 'user-is_superuser', 'profile-expiration_date']

        user = User.objects.get(username=username)
        if user != request.user and not request.user.is_staff:
            mess = ugettext('Access not allowed')
            title = ugettext('User profile') + ' : ' + username + ' : ' + mess
            description = ugettext('Please login or contact the website administator to get a private access.')
            messages.error(request, title)
            return render(request, 'telemeta/messages.html', {'description' : description})

        try:
            profile = user.get_profile()
        except:
            profile = UserProfile(user=user)

        if request.method == 'POST':
            user_form = UserChangeForm(request.POST, instance=user, prefix='user')
            profile_form = UserProfileForm(request.POST, instance=profile, prefix='profile')
            if user_form.is_valid() and profile_form.is_valid():
                user_form.save()
                profile_form.save()
                return HttpResponseRedirect('/users/'+username+'/profile/')
        else:
            user_form = UserChangeForm(instance=user, prefix='user')
            profile_form = UserProfileForm(instance=profile, prefix='profile')
            forms = [user_form, profile_form]
        return render(request, template, {'forms': forms, 'usr': user, 'user_hidden_fields': user_hidden_fields})


class LastestRevisionsFeed(Feed):
    "the RSS feed of the lastest revisions"

    organization = settings.TELEMETA_ORGANIZATION
    subjects = settings.TELEMETA_SUBJECTS
    tags = ['title', 'description', 'comment']
    title = organization + ' - Telemeta - ' + ugettext('Last changes')
    link = ""
    description = ' '.join([subject.decode('utf-8') for subject in subjects])
    n_items = 100

    def items(self):
        return get_revisions(self.n_items)

    def item_title(self, r):
        element = r['element']
        if element.title == '':
            title = str(element.public_id)
        else:
            title = element.title
        return element.element_type + ' : ' + title

    def item_description(self, r):
        revision = r['revision']
        element = r['element']
        description = '<b>modified by ' + revision.user.username + ' on ' + unicode(revision.time) + '</b><br /><br />'
        dict = element.to_dict()
        for tag in dict.keys():
            try:
                value = dict[tag]
                if value != '':
                    description += tag + ' : ' + value + '<br />'
            except:
                continue
        return description.encode('utf-8')

    def item_link(self, r):
        revision = r['revision']
        element = r['element']
        link = '/' + revision.element_type + 's/' + str(element.public_id)
        return link


class UserRevisionsFeed(LastestRevisionsFeed):

    def get_object(self, request, username):
        return get_object_or_404(User, username=username)

    def items(self, obj):
        return get_revisions(self.n_items, obj)


class ResourceView(object):
    """Provide Resource web UI methods"""

    types = {'corpus':
                {'model': MediaCorpus,
                'form' : MediaCorpusForm,
                'related': MediaCorpusRelated,
                'related_form': MediaCorpusRelatedForm,
                'parent': MediaFonds,
                },
            'fonds':
                {'model': MediaFonds,
                'form' : MediaFondsForm,
                'related': MediaFondsRelated,
                'related_form': MediaFondsRelatedForm,
                'parent': None,
                }
            }

    def setup(self, type):
        self.model = self.types[type]['model']
        self.form = self.types[type]['form']
        self.related = self.types[type]['related']
        self.related_form = self.types[type]['related_form']
        self.parent = self.types[type]['parent']
        self.type = type

    def detail(self, request, type, public_id, template='telemeta/resource_detail.html'):
        self.setup(type)
        resource = self.model.objects.get(code=public_id)
        children = resource.children.all()
        children = children.order_by('code')
        related_media = self.related.objects.filter(resource=resource)
        check_related_media(related_media)
        playlists = get_playlists(request)
        if self.parent:
            parents = self.parent.objects.filter(children=resource)
        else:
            parents = []

        return render(request, template, {'resource': resource, 'type': type, 'children': children, 'related_media': related_media, 'parents': parents, 'playlists': playlists })

    @jsonrpc_method('telemeta.change_fonds')
    @jsonrpc_method('telemeta.change_corpus')
    def edit(self, request, type, public_id, template='telemeta/resource_edit.html'):
        self.setup(type)
        resource = self.model.objects.get(code=public_id)
        if request.method == 'POST':
            form = self.form(data=request.POST, files=request.FILES, instance=resource)
            if form.is_valid():
                code = form.cleaned_data['code']
                if not code:
                    code = public_id
                form.save()
                resource.set_revision(request.user)
                return HttpResponseRedirect('/archives/'+self.type+'/'+code)
        else:
            form = self.form(instance=resource)
        return render(request, template, {'resource': resource, 'type': type, 'form': form,})

    @jsonrpc_method('telemeta.add_fonds')
    @jsonrpc_method('telemeta.add_corpus')
    def add(self, request, type, template='telemeta/resource_add.html'):
        self.setup(type)
        resource = self.model()
        if request.method == 'POST':
            form = self.form(data=request.POST, files=request.FILES, instance=resource)
            if form.is_valid():
                code = form.cleaned_data['code']
                if not code:
                    code = public_id
                form.save()
                resource.set_revision(request.user)
                return HttpResponseRedirect('/archives/'+self.type +'/'+code)
        else:
            form = self.form(instance=resource)
        return render(request, template, {'resource': resource, 'type': type, 'form': form,})

    @jsonrpc_method('telemeta.add_fonds')
    @jsonrpc_method('telemeta.add_corpus')
    def copy(self, request, type, public_id, template='telemeta/resource_edit.html'):
        self.setup(type)
        if request.method == 'POST':
            resource = self.model()
            form = self.form(data=request.POST, files=request.FILES, instance=resource)
            if form.is_valid():
                code = form.cleaned_data['code']
                if not code:
                    code = public_id
                resource.save()
                resource.set_revision(request.user)
                return HttpResponseRedirect('/archives/'+self.type +'/'+code)
        else:
            resource = self.model.objects.get(code=public_id)
            form = self.form(instance=resource)
        return render(request, template, {'resource': resource, 'type': type, "form": form,})

    def playlist(self, request, type, public_id, template, mimetype):
        self.setup(type)
        try:
            resource = self.model.objects.get(code=public_id)
        except ObjectDoesNotExist:
            raise Http404

        template = loader.get_template(template)
        context = RequestContext(request, {'resource': resource, 'host': request.META['HTTP_HOST']})
        return HttpResponse(template.render(context), mimetype=mimetype)

    @jsonrpc_method('telemeta.del_fonds')
    @jsonrpc_method('telemeta.del_corpus')
    def delete(self, request, type, public_id):
        self.setup(type)
        resource = self.model.objects.get(code=public_id)
        resource.delete()
        return HttpResponseRedirect('/archives/'+self.type+'/')

    def related_stream(self, request, type, public_id, media_id):
        self.setup(type)
        resource = self.model.objects.get(code=public_id)
        media = self.related.objects.get(resource=resource, id=media_id)
        response = HttpResponse(stream_from_file(media.file.path), mimetype=media.mime_type)
        return response

    @jsonrpc_method('telemeta.add_fonds_related_media')
    @jsonrpc_method('telemeta.add_corpus_related_media')
    def related_edit(self, request, type, public_id, template):
        self.setup(type)
        resource = self.model.objects.get(code=public_id)
        ResourceRelatedFormSet = inlineformset_factory(self.model, self.related, form=self.related_form)
        if request.method == 'POST':
            formset = ResourceRelatedFormSet(data=request.POST, files=request.FILES, instance=resource)
            if formset.is_valid():
                formset.save()
                resource.set_revision(request.user)
                return HttpResponseRedirect('/archives/'+self.type+'/'+public_id)
        else:
            formset = ResourceRelatedFormSet(instance=resource)
        return render(request, template, {'resource': resource, 'type': type, 'formset': formset,})



# -*- coding: utf-8 -*-
# Copyright (C) 2007 Samalyse SARL

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

# Author: Olivier Guilyardi <olivier@samalyse.com>

import re
import os
import sys
import datetime
import timeside

from django.template import RequestContext, loader
from django import template
from django.http import HttpResponse
from django.http import Http404
from django.shortcuts import render_to_response, redirect
from django.views.generic import list_detail
from django.conf import settings
from django.contrib import auth
from django.contrib.auth.decorators import login_required

from telemeta.models import MediaItem, Location, MediaCollection, EthnicGroup
from telemeta.models import dublincore, Enumeration
import telemeta.interop.oai as oai
from telemeta.interop.oaidatasource import TelemetaOAIDataSource
from django.core.exceptions import ObjectDoesNotExist
from telemeta.util.unaccent import unaccent
from telemeta.web import pages
from telemeta.util.unaccent import unaccent_icmp

def render(request, template, data = None, mimetype = None):
    return render_to_response(template, data, context_instance=RequestContext(request), 
                              mimetype=mimetype)

def stream(file):
    chunk_size = 0x10000
    f = open(file,  'r')
    while True:
        _chunk = f.read(chunk_size)
        if not len(_chunk):
            break
        yield _chunk
    f.close()


class WebView:
    """Provide web UI methods"""

    graphers = timeside.processors(timeside.api.IGrapher)
    decoders = timeside.processors(timeside.api.IDecoder)
    encoders= timeside.processors(timeside.api.IEncoder)
    analyzers = timeside.processors(timeside.api.IAnalyzer)
    
    def index(self, request):
        """Render the homepage"""

        template = loader.get_template('telemeta/index.html')
        ids = [id for id in MediaItem.objects.all().values_list('id', flat=True).order_by('?')[0:4]]
        items = MediaItem.objects.enriched().filter(pk__in=ids)

        context = RequestContext(request, {
                    'page_content': pages.get_page_content(request, 'parts/home', ignore_slash_issue=True),
                    'items': items})
        return HttpResponse(template.render(context))

    def collection_detail(self, request, public_id, template=''):
        collection = MediaCollection.objects.get(public_id=public_id)
        return render(request, template, {'collection': collection})


    def item_detail(self, request, public_id, template='telemeta/mediaitem_detail.html'):
        """Show the details of a given item"""
        item = MediaItem.objects.get(public_id=public_id)
        
        formats = []
        for encoder in self.encoders:
            formats.append({'name': encoder.format(), 'extension': encoder.file_extension()})

        graphers = []
        for grapher in self.graphers:
            graphers.append({'name':grapher.name(), 'id': grapher.id()})
        if request.REQUEST.has_key('grapher_id'):
            grapher_id = request.REQUEST['grapher_id']
        else:
            grapher_id = 'waveform'
        
        analyzers = [{'name':'','id':'','unit':'','value':''}]
        # TODO: override timeside analyzer process when caching
        self.analyzer_mode = 0
        
        if self.analyzer_mode:
            analyzers_sub = []
            if item.file:
                audio = os.path.join(os.path.dirname(__file__), item.file.path)
                decoder  = timeside.decoder.FileDecoder(audio)
                self.pipe = decoder
                for analyzer in self.analyzers:
                    subpipe = analyzer()
                    analyzers_sub.append(subpipe)
                    self.pipe = self.pipe | subpipe
                self.pipe.run()
                
            for analyzer in analyzers_sub:
                if item.file:
                    value = analyzer.result()
                    if analyzer.id() == 'duration':
                        approx_value = int(round(value))
                        item.approx_duration = approx_value
                        item.save()
                        value = datetime.timedelta(0,value)
                else:
                    value = 'N/A'

                analyzers.append({'name':analyzer.name(),
                                  'id':analyzer.id(),
                                  'unit':analyzer.unit(),
                                  'value':str(value)})

        return render(request, template, 
                    {'item': item, 'export_formats': formats, 
                    'visualizers': graphers, 'visualizer_id': grapher_id,'analysers': analyzers,
                    'audio_export_enabled': getattr(settings, 'TELEMETA_DOWNLOAD_ENABLED', False)
                    })

    def item_visualize(self, request, public_id, visualizer_id, width, height):
        grapher_id = visualizer_id
        for grapher in self.graphers:
            if grapher.id() == grapher_id:
                break

        if grapher.id() != grapher_id:
            raise Http404

        media = settings.TELEMETA_DATA_CACHE_DIR + \
                    os.sep + '_'.join([public_id,  grapher_id,  width,  height]) + '.png'
        #graph.set_colors((255,255,255), 'purple')
        
        if not os.path.exists(media):
            item = MediaItem.objects.get(public_id=public_id)
            audio = os.path.join(os.path.dirname(__file__), item.file.path)
            decoder  = timeside.decoder.FileDecoder(audio)
            graph = grapher(width=int(width), height=int(height), output=media)
            (decoder | graph).run()
            graph.render()
        response = HttpResponse(stream(media), mimetype = 'image/png')
        return response

    def list_export_extensions(self):
        "Return the recognized item export file extensions, as a list"
        list = []
        for encoder in self.encoders:
            list.append(encoder.file_extension())
        return list

    def item_export(self, request, public_id, extension):                    
        """Export a given media item in the specified format (OGG, FLAC, ...)"""

        if extension != 'mp3' and not getattr(settings, 'TELEMETA_DOWNLOAD_ENABLED', False):
            raise Http404 # FIXME: should be some sort of permissions denied error

        for encoder in self.encoders:
            if encoder.file_extension() == extension:
                break

        if encoder.file_extension() != extension:
            raise Http404('Unknown export file extension: %s' % extension)

        mime_type = encoder.mime_type()
        cache_dir = settings.TELEMETA_EXPORT_CACHE_DIR
        media = cache_dir + os.sep + public_id + '.' + encoder.file_extension()
        
        item = MediaItem.objects.get(public_id=public_id)
        audio = os.path.join(os.path.dirname(__file__), item.file.path)
        decoder  = timeside.decoder.FileDecoder(audio)
        print decoder.format(),  mime_type
        if decoder.format() == mime_type:
            # source > stream
            media = audio
        else:        
            if not os.path.exists(media):
                # source > encoder > stream
                decoder  = timeside.decoder.FileDecoder(audio)
                enc = encoder(media)
                metadata = dublincore.express_item(item).to_list()
                #enc.set_metadata(metadata)
                (decoder | enc).run()
            
        response = HttpResponse(stream(media), mimetype = mime_type)
        response['Content-Disposition'] = 'attachment'
        return response

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

    def search(self, request, type = None):
        """Perform a search through collections and items metadata"""
        collections = MediaCollection.objects.enriched()
        items = MediaItem.objects.enriched()
        input = request.REQUEST
        criteria = {}

        switch = {
            'pattern': lambda value: ( 
                collections.quick_search(value), 
                items.quick_search(value)),
            'title': lambda value: (
                collections.word_search('title', value), 
                items.by_title(value)),
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
        }
       
        for key, value in input.items():
            func = switch.get(key)
            if func and value and value != "0":
                try:
                    res = func(value)
                    if len(res) > 2:
                        collections, items, value = res
                    else: 
                        collections, items = res
                except ObjectDoesNotExist:
                    collections = collections.none()
                    items = items.none()

                criteria[key] = value

        if type is None:
            if collections.count() and not items.count():
                type = 'collections'
            else:
                type = 'items'

        if type == 'items':
            objects = items
        else:
            objects = collections

        return list_detail.object_list(request, objects, 
            template_name='telemeta/search_results.html', paginate_by=20,
            extra_context={'criteria': criteria, 'collections_num': collections.count(), 
                'items_num': items.count(), 'type' : type})

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

    @login_required
    def admin_index(self, request):
        return render(request, 'telemeta/admin.html', self. __get_admin_context_vars())

    def __get_enumeration(self, id):
        from django.db.models import get_models
        models = get_models(telemeta.models)
        for model in models:
            if model._meta.module_name == id:
                break

        if model._meta.module_name != id:
            return None

        return model

    @login_required
    def edit_enumeration(self, request, enumeration_id):        

        enumeration  = self.__get_enumeration(enumeration_id)
        if enumeration == None:
            raise Http404

        vars = self.__get_admin_context_vars()
        vars["enumeration_id"] = enumeration._meta.module_name
        vars["enumeration_name"] = enumeration._meta.verbose_name            
        vars["enumeration_values"] = enumeration.objects.all()
        return render(request, 'telemeta/enumeration_edit.html', vars)

    @login_required
    def add_to_enumeration(self, request, enumeration_id):        

        enumeration  = self.__get_enumeration(enumeration_id)
        if enumeration == None:
            raise Http404

        enumeration_value = enumeration(value=request.POST['value'])
        enumeration_value.save()

        return self.edit_enumeration(request, enumeration_id)

    @login_required
    def update_enumeration(self, request, enumeration_id):        
        
        enumeration  = self.__get_enumeration(enumeration_id)
        if enumeration == None:
            raise Http404

        if request.POST.has_key("remove"):
            enumeration.objects.filter(id__in=request.POST.getlist('sel')).delete()

        return self.edit_enumeration(request, enumeration_id)

    @login_required
    def edit_enumeration_value(self, request, enumeration_id, value_id):        

        enumeration  = self.__get_enumeration(enumeration_id)
        if enumeration == None:
            raise Http404
        
        vars = self.__get_admin_context_vars()
        vars["enumeration_id"] = enumeration._meta.module_name
        vars["enumeration_name"] = enumeration._meta.verbose_name            
        vars["enumeration_record"] = enumeration.objects.get(id__exact=value_id)
        return render(request, 'telemeta/enumeration_edit_value.html', vars)

    @login_required
    def update_enumeration_value(self, request, enumeration_id, value_id):        

        if request.POST.has_key("save"):
            enumeration  = self.__get_enumeration(enumeration_id)
            if enumeration == None:
                raise Http404
       
            record = enumeration.objects.get(id__exact=value_id)
            record.value = request.POST["value"]
            record.save()

        return self.edit_enumeration(request, enumeration_id)
  
    def collection_playlist(self, request, public_id, template, mimetype):
        try:
            collection = MediaCollection.objects.get(public_id=public_id)
        except ObjectDoesNotExist:
            raise Http404

        template = loader.get_template(template)
        context = RequestContext(request, {'collection': collection, 'host': request.META['HTTP_HOST']})
        return HttpResponse(template.render(context), mimetype=mimetype)

    def item_playlist(self, request, public_id, template, mimetype):
        try:
            item = MediaItem.objects.get(public_id=public_id)
        except ObjectDoesNotExist:
            raise Http404

        template = loader.get_template(template)
        context = RequestContext(request, {'item': item, 'host': request.META['HTTP_HOST']})
        return HttpResponse(template.render(context), mimetype=mimetype)

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

    def handle_oai_request(self, request):
        url         = 'http://' + request.META['HTTP_HOST'] + request.path
        datasource  = TelemetaOAIDataSource()
        admin       = settings.ADMINS[0][1]
        provider    = oai.DataProvider(datasource, "Telemeta", url, admin)
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

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

from django.template import Context, loader
from django import template
from django.http import HttpResponse
from django.http import Http404
from django.shortcuts import render_to_response, redirect
from django.views.generic import list_detail
from django.conf import settings

import telemeta
from telemeta.models import MediaItem, Location, MediaCollection
from telemeta.models import dublincore
from telemeta.core import Component, ExtensionPoint
from telemeta.export import *
from telemeta.visualization import *
from telemeta.analysis import *
from telemeta.analysis.vamp import *
import telemeta.interop.oai as oai
from telemeta.interop.oaidatasource import TelemetaOAIDataSource
from django.core.exceptions import ObjectDoesNotExist
from telemeta.util.unaccent import unaccent
from telemeta.web import pages

class WebView(Component):
    """Provide web UI methods"""

    exporters = ExtensionPoint(IExporter)
    visualizers = ExtensionPoint(IMediaItemVisualizer)
    analyzers = ExtensionPoint(IMediaItemAnalyzer)

    def index(self, request):
        """Render the homepage"""

        template = loader.get_template('telemeta/index.html')
        context = Context({'page_content': pages.get_page_content(request, 'parts/home', True)})
        return HttpResponse(template.render(context))

    def collection_detail(self, request, public_id, template=''):
        collection = MediaCollection.objects.get(public_id=public_id)
        return render_to_response(template, {'collection': collection})


    def item_detail(self, request, public_id, template='telemeta/mediaitem_detail.html'):
        """Show the details of a given item"""
        item = MediaItem.objects.get(public_id=public_id)
        
        formats = []
        for exporter in self.exporters:
            formats.append({'name': exporter.get_format(), 'extension': exporter.get_file_extension()})

        visualizers = []
        for visualizer in self.visualizers:
            visualizers.append({'name':visualizer.get_name(), 'id':
                visualizer.get_id()})
        if request.REQUEST.has_key('visualizer_id'):
            visualizer_id = request.REQUEST['visualizer_id']
        else:
            visualizer_id = 'waveform_audiolab'

        analyzers = []
        for analyzer in self.analyzers:
            if item.file:
                value = analyzer.render(item)
            else:
                value = 'N/A'

            analyzers.append({'name':analyzer.get_name(),
                              'id':analyzer.get_id(),
                              'unit':analyzer.get_unit(),
                              'value':str(value)})

        vamp = VampCoreAnalyzer()
        vamp_plugins = vamp.get_plugins_list()
        vamp_plugin_list = []
        for plugin in vamp_plugins:
            vamp_plugin_list.append(':'.join(plugin[1:]))
          
        return render_to_response(template, 
                    {'item': item, 'export_formats': formats, 
                    'visualizers': visualizers, 'visualizer_id': visualizer_id,
                    'analysers': analyzers, 'vamp_plugins': vamp_plugin_list})
                    
    def item_visualize(self, request, public_id, visualizer_id, width, height):
        for visualizer in self.visualizers:
            if visualizer.get_id() == visualizer_id:
                break

        if visualizer.get_id() != visualizer_id:
            raise Http404
        
        item = MediaItem.objects.get(public_id=public_id)

        visualizer.set_colors((255,255,255), 'purple')
        stream = visualizer.render(item, width=int(width), height=int(height))
        response = HttpResponse(stream, mimetype = 'image/png')
        return response

    def list_export_extensions(self):
        "Return the recognized item export file extensions, as a list"
        list = []
        for exporter in self.exporters:
            list.append(exporter.get_file_extension())
        return list

    def item_export(self, request, public_id, extension):                    
        """Export a given media item in the specified format (OGG, FLAC, ...)"""
        for exporter in self.exporters:
            if exporter.get_file_extension() == extension:
                break

        if exporter.get_file_extension() != extension:
            raise Http404('Unknown export file extension: %s' % extension)

        mime_type = exporter.get_mime_type()

        exporter.set_cache_dir(settings.TELEMETA_EXPORT_CACHE_DIR)

        item = MediaItem.objects.get(public_id=public_id)

        infile = item.file.path
        metadata = dublincore.express_item(item).flatten()
        stream = exporter.process(item.id, infile, metadata)

        response = HttpResponse(stream, mimetype = mime_type)
        response['Content-Disposition'] = 'attachment'
        return response

    def edit_search(self, request):
        ethnic_groups = MediaItem.objects.all().ethnic_groups()
        return render_to_response('telemeta/search_criteria.html', 
            {'ethnic_groups': ethnic_groups})

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
                items.filter(ethnie_grsocial = value)),
            'creator': lambda value: (
                collections.word_search('creator', value),
                items.word_search('auteur', value)),
            'rec_date': lambda value: (
                collections.by_recording_date(value), 
                items.by_recording_date(value)),
            'pub_date': lambda value: (
                collections.by_publish_date(value), 
                items.by_publish_date(value))
        }
       
        for key, value in input.items():
            if key == 'continent' and input.get('country'):
                continue
            func = switch.get(key)
            if func and value:
                collections, items = func(value)
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
            if getattr(model, "is_enumeration", False):
                enumerations.append({"name": model._meta.verbose_name_plural, 
                    "id": model._meta.module_name})
        return enumerations                    
    
    def __get_admin_context_vars(self):
        return {"enumerations": self.__get_enumerations_list()}

    def admin_index(self, request):
        return render_to_response('telemeta/admin.html', self. __get_admin_context_vars())

    def __get_enumeration(self, id):
        from django.db.models import get_models
        models = get_models(telemeta.models)
        for model in models:
            if model._meta.module_name == id:
                break

        if model._meta.module_name != id:
            return None

        return model

    def edit_enumeration(self, request, enumeration_id):        

        enumeration  = self.__get_enumeration(enumeration_id)
        if enumeration == None:
            raise Http404

        vars = self.__get_admin_context_vars()
        vars["enumeration_id"] = enumeration._meta.module_name
        vars["enumeration_name"] = enumeration._meta.verbose_name            
        vars["enumeration_name_plural"] = enumeration._meta.verbose_name_plural
        vars["enumeration_values"] = enumeration.objects.all()
        return render_to_response('telemeta/enumeration_edit.html', vars)

    def add_to_enumeration(self, request, enumeration_id):        

        enumeration  = self.__get_enumeration(enumeration_id)
        if enumeration == None:
            raise Http404

        enumeration_value = enumeration(value=request.POST['value'])
        enumeration_value.save()

        return self.edit_enumeration(request, enumeration_id)

    def update_enumeration(self, request, enumeration_id):        
        
        enumeration  = self.__get_enumeration(enumeration_id)
        if enumeration == None:
            raise Http404

        if request.POST.has_key("remove"):
            enumeration.objects.filter(id__in=request.POST.getlist('sel')).delete()

        return self.edit_enumeration(request, enumeration_id)

    def edit_enumeration_value(self, request, enumeration_id, value_id):        

        enumeration  = self.__get_enumeration(enumeration_id)
        if enumeration == None:
            raise Http404
        
        vars = self.__get_admin_context_vars()
        vars["enumeration_id"] = enumeration._meta.module_name
        vars["enumeration_name"] = enumeration._meta.verbose_name            
        vars["enumeration_name_plural"] = enumeration._meta.verbose_name_plural
        vars["enumeration_record"] = enumeration.objects.get(id__exact=value_id)
        return render_to_response('telemeta/enumeration_edit_value.html', vars)

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
        context = Context({'collection': collection, 'host': request.META['HTTP_HOST']})
        return HttpResponse(template.render(context), mimetype=mimetype)

    def item_playlist(self, request, public_id, template, mimetype):
        try:
            item = MediaItem.objects.get(public_id=public_id)
        except ObjectDoesNotExist:
            raise Http404

        template = loader.get_template(template)
        context = Context({'item': item, 'host': request.META['HTTP_HOST']})
        return HttpResponse(template.render(context), mimetype=mimetype)

    def list_continents(self, request):
        continents = MediaItem.objects.all().countries(group_by_continent=True)
        return render_to_response('telemeta/geo_continents.html', 
                    {'continents': continents, 'gmap_key': settings.TELEMETA_GMAP_KEY })

    def country_info(self, request, id):
        country = Location.objects.get(pk=id)
        return render_to_response('telemeta/country_info.html', {
            'country': country, 'continent': country.continents()[0]})

    def list_countries(self, request, continent):                    
        continent = Location.objects.by_flatname(continent)[0]
        data = MediaCollection.objects.stat_continents(only_continent=continent)

        return render_to_response('telemeta/geo_countries.html', {'continent': data[0] })

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
            return render_to_response('telemeta/flatpage.html', {'page_content': content })
        

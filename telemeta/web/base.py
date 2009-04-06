# Copyright (C) 2007 Samalyse SARL
# All rights reserved.
#
# This software is licensed as described in the file COPYING, which
# you should have received as part of this distribution. The terms
# are also available at http://svn.parisson.org/telemeta/TelemetaLicense.
#
# Author: Olivier Guilyardi <olivier@samalyse.com>

import re
import os
import sys

from django.template import Context, loader
from django import template
from django.http import HttpResponse
from django.http import Http404
from django.shortcuts import render_to_response
from django.views.generic import list_detail
from django.conf import settings

import telemeta
from telemeta.models import MediaItem
from telemeta.models import MediaCollection
from telemeta.core import Component, ExtensionPoint
from telemeta.export import *
from telemeta.visualization import *
from telemeta.analysis import *
from telemeta.analysis.vamp import *
import telemeta.interop.oai as oai
from telemeta.interop.oaidatasource import TelemetaOAIDataSource

class WebView(Component):
    """Provide web UI methods"""

    exporters = ExtensionPoint(IExporter)
    visualizers = ExtensionPoint(IMediaItemVisualizer)
    analyzers = ExtensionPoint(IMediaItemAnalyzer)

    def index(self, request):
        """Render the homepage"""

        template = loader.get_template('telemeta/index.html')
        context = Context({})
        return HttpResponse(template.render(context))

    def item_detail(self, request, item_id, template='telemeta/mediaitem_detail.html'):
        """Show the details of a given item"""
        item = MediaItem.objects.get(pk=item_id)
        
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
            value = analyzer.render(item)
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
                    
    def item_visualize(self, request, item_id, visualizer_id, width, height):
        for visualizer in self.visualizers:
            if visualizer.get_id() == visualizer_id:
                break

        if visualizer.get_id() != visualizer_id:
            raise Http404
        
        item = MediaItem.objects.get(pk=item_id)

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

    def item_export(self, request, item_id, extension):                    
        """Export a given media item in the specified format (OGG, FLAC, ...)"""
        for exporter in self.exporters:
            if exporter.get_file_extension() == extension:
                break

        if exporter.get_file_extension() != extension:
            raise Http404('Unknown export file extension: %s' % extension)

        mime_type = exporter.get_mime_type()

        exporter.set_cache_dir(settings.TELEMETA_EXPORT_CACHE_DIR)

        item = MediaItem.objects.get(pk=item_id)

        infile = item.file.path
        metadata = item.to_dublincore().flatten()
        stream = exporter.process(item.id, infile, metadata)

        response = HttpResponse(stream, mimetype = mime_type)
        response['Content-Disposition'] = 'attachment'
        return response

    def edit_search(self, request):
        continents = MediaCollection.objects.list_continents()
        countries = MediaCollection.objects.list_countries()
        ethnic_groups = MediaItem.objects.list_ethnic_groups()
        return render_to_response('telemeta/search_criteria.html', 
            {'continents': continents, 'countries': countries, 
            'ethnic_groups': ethnic_groups})

    def search(self, request, type = None):
        """Perform a search through collections and items metadata"""
        collections = MediaCollection.objects.all()
        items = MediaItem.objects.all()
        input = request.REQUEST
        criteria = {}

        switch = {
            'pattern': lambda value: ( 
                collections.quick_search(value), 
                items.quick_search(value)),
            'title': lambda value: (
                collections.word_search('title', value), 
                items.by_title(value)),
            'country': lambda value: (
                collections.by_country(value), 
                items.filter(etat = value)),
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
  
    def collection_playlist(self, request, collection_id, template, mimetype):
        collection = MediaCollection.objects.get(id__exact=collection_id)
        if not collection:
            raise Http404

        template = loader.get_template(template)
        context = Context({'collection': collection, 'host': request.META['HTTP_HOST']})
        return HttpResponse(template.render(context), mimetype=mimetype)

    def item_playlist(self, request, item_id, template, mimetype):
        item = MediaItem.objects.get(id__exact=item_id)
        if not item:
            raise Http404

        template = loader.get_template(template)
        context = Context({'item': item, 'host': request.META['HTTP_HOST']})
        return HttpResponse(template.render(context), mimetype=mimetype)

    def list_continents(self, request):
        continents = MediaCollection.objects.stat_continents()
        return render_to_response('telemeta/geo_continents.html', 
                    {'continents': continents })

    def get_continents_js(self, request):
        countries = MediaCollection.objects.list_countries()
        return render_to_response('telemeta/geo_continents.js', 
                    {'countries': countries})

    def list_countries(self, request, continent):                    
        continents = MediaCollection.objects.stat_continents()
        for c in continents:
            if c["name"] == continent:
                break
        if c["name"] != continent:
            raise Http404

        return render_to_response('telemeta/geo_countries.html', {'continent': c })

    def list_country_collections(self, request, continent, country):
        objects = MediaCollection.objects.by_country(country)
        return list_detail.object_list(request, objects, 
            template_name='telemeta/geo_country_collections.html', paginate_by=20,
            extra_context={'country': country, 'continent': continent})

    def handle_oai_request(self, request):
        url = request.META['HTTP_HOST'] + request.path
        datasource  = TelemetaOAIDataSource()
        provider    = oai.DataProvider(datasource, "Telemeta", url, "admin@telemeta.org")
        args = request.GET.copy()
        args.update(request.POST)
        return HttpResponse(provider.handle(args), mimetype='text/xml')
        


# Copyright (C) 2007 Samalyse SARL
# All rights reserved.
#
# This software is licensed as described in the file COPYING, which
# you should have received as part of this distribution. The terms
# are also available at http://svn.parisson.org/telemeta/TelemetaLicense.
#
# Author: Olivier Guilyardi <olivier@samalyse.com>

import telemeta
from django.template import Context, loader
from django import template
from django.http import HttpResponse
from django.http import Http404
from telemeta.models import MediaItem
from telemeta.models import MediaCollection
from django.shortcuts import render_to_response
import re
from telemeta.core import *
from telemeta.export import *
from telemeta.visualization import *
from django.conf import settings
import os

class WebView(Component):
    """Provide web UI methods"""

    exporters = ExtensionPoint(IExporter)
    visualizers = ExtensionPoint(IMediaItemVisualizer)

    def index(self, request):
        """Render the homepage"""

        template = loader.get_template('index.html')
        context = Context({})
        return HttpResponse(template.render(context))

    def item_detail(self, request, item_id):
        """Show the details of a given item"""
        item = MediaItem.objects.get(pk=item_id)
        formats = []
        for exporter in self.exporters:
            formats.append(exporter.get_format())
        visualizers = []
        for visualizer in self.visualizers:
            visualizers.append({'name':visualizer.get_name(), 'id': 
                visualizer.get_id()})
        if request.REQUEST.has_key('visualizer_id'):
            visualizer_id = request.REQUEST['visualizer_id']
        else:
            visualizer_id = 'waveform'
        return render_to_response('mediaitem_detail.html', 
                    {'item': item, 'export_formats': formats, 
                    'visualizers': visualizers, 'visualizer_id': visualizer_id})
                    
    def item_visualize(self, request, item_id, visualizer_id):
        for visualizer in self.visualizers:
            if visualizer.get_id() == visualizer_id:
                break

        if visualizer.get_id() != visualizer_id:
            raise Http404
        
        item = MediaItem.objects.get(pk=item_id)

        stream = visualizer.render(item)
        response = HttpResponse(stream, mimetype = 'image/png')
        return response


    def __file_stream(self, filepath):
        """Generator for streaming a file from the disk. 
        
        This method shouldn't be needed anymore when bug #8 get fixed
        """

        buffer_size = 0xFFFF
        f = open(filepath, 'rb')
        chunk = f.read(buffer_size)
        yield chunk
        while chunk:
            chunk = f.read(buffer_size)
            yield chunk
        f.close()            

    def item_export(self, request, item_id, format):                    
        """Export a given media item in the specified format (OGG, FLAC, ...)"""
        for exporter in self.exporters:
            if exporter.get_format() == format:
                break

        if exporter.get_format() != format:
            raise Http404

        mime_type = exporter.get_mime_type()

        exporter.set_cache_dir(settings.TELEMETA_EXPORT_CACHE_DIR)

        item = MediaItem.objects.get(pk=item_id)

        infile = settings.MEDIA_ROOT + "/" + item.file
        metadata = item.to_dict()
        metadata['collection'] = str(metadata['collection'])
        metadata['Collection'] = metadata['collection']
        metadata['Artist'] = metadata['creator']
        metadata['Title'] = metadata['title']

        outfile = exporter.process(item.id, infile, metadata, [])

        response = HttpResponse(self.__file_stream(outfile), mimetype = mime_type)
        response['Content-Disposition'] = 'attachment; filename="download.' + \
                    exporter.get_file_extension() + '"'
        return response

    def quick_search(self, request):
        """Perform a simple search through collections and items core metadata"""
        pattern = request.REQUEST["pattern"]
        collections = MediaCollection.objects.quick_search(pattern)
        items = MediaItem.objects.quick_search(pattern)
        return render_to_response('search_results.html', 
                    {'pattern': pattern, 'collections': collections, 
                     'items': items})

    def __get_dictionary_list(self):
        from django.db.models import get_models
        models = get_models(telemeta.models)

        dictionaries = []
        for model in models:
            if getattr(model, "is_dictionary", False):
                dictionaries.append({"name": model._meta.verbose_name_plural, 
                    "id": model._meta.module_name})
        return dictionaries                    
    
    def __get_admin_context_vars(self):
        return {"dictionaries": self.__get_dictionary_list()}

    def admin_index(self, request):
        return render_to_response('admin.html', self. __get_admin_context_vars())

    def __get_dictionary(self, id):
        from django.db.models import get_models
        models = get_models(telemeta.models)
        for model in models:
            if model._meta.module_name == id:
                break

        if model._meta.module_name != id:
            return None

        return model
        

    def edit_dictionary(self, request, dictionary_id):        

        dictionary  = self.__get_dictionary(dictionary_id)
        if dictionary == None:
            raise Http404

        vars = self.__get_admin_context_vars()
        vars["dictionary_id"] = dictionary._meta.module_name
        vars["dictionary_name"] = dictionary._meta.verbose_name            
        vars["dictionary_name_plural"] = dictionary._meta.verbose_name_plural
        vars["dictionary_values"] = dictionary.objects.all()
        return render_to_response('dictionary_edit.html', vars)

    def add_to_dictionary(self, request, dictionary_id):        

        dictionary  = self.__get_dictionary(dictionary_id)
        if dictionary == None:
            raise Http404

        dictionary_value = dictionary(value=request.POST['value'])
        dictionary_value.save()

        return self.edit_dictionary(request, dictionary_id)

    def update_dictionary(self, request, dictionary_id):        
        
        dictionary  = self.__get_dictionary(dictionary_id)
        if dictionary == None:
            raise Http404

        if request.POST.has_key("remove"):
            dictionary.objects.filter(id__in=request.POST['sel']).delete()

        return self.edit_dictionary(request, dictionary_id)

    def edit_dictionary_value(self, request, dictionary_id, value_id):        

        dictionary  = self.__get_dictionary(dictionary_id)
        if dictionary == None:
            raise Http404
        
        vars = self.__get_admin_context_vars()
        vars["dictionary_id"] = dictionary._meta.module_name
        vars["dictionary_name"] = dictionary._meta.verbose_name            
        vars["dictionary_name_plural"] = dictionary._meta.verbose_name_plural
        vars["dictionary_record"] = dictionary.objects.get(id__exact=value_id)
        return render_to_response('dictionary_edit_value.html', vars)

    def update_dictionary_value(self, request, dictionary_id, value_id):        

        if request.POST.has_key("save"):
            dictionary  = self.__get_dictionary(dictionary_id)
            if dictionary == None:
                raise Http404
       
            record = dictionary.objects.get(id__exact=value_id)
            record.value = request.POST["value"]
            record.save()

        return self.edit_dictionary(request, dictionary_id)

        
def media_item_edit(request, media_item_id):
    "Provide MediaItem object edition"

    media_item = MediaItem.objects.get(pk=media_item_id)
    dynprops = media_item.get_dynamic_properties()
    return render_to_response('media_item.html', {'media_item': media_item, 'dynprops' : dynprops})

def media_item_update(request, media_item_id):
    "Handle MediaItem object edition form submission"

    media_item = MediaItem.objects.get(pk=media_item_id)
    media_item.author = request.POST['author']
    media_item.title = request.POST['title']
    media_item.save()

    pattern = re.compile(r'^dynprop_(\d+)$')
    for name, value in request.POST.items():
        match = pattern.search(name)
        if match:
            prop_id = match.groups()[0]
            prop = MediaItemPropertyDefinition.objects.get(pk=prop_id)
            telemeta.logger.debug("prop_id: " + prop_id + " ; " + "media_item_id: " + 
                                    media_item_id + " ; value: " + value + 
                                    " ; type:" + prop.type)
            media_item = MediaItem.objects.get(pk=media_item_id)
            property, created = MediaItemProperty.objects.get_or_create(
                                    media_item=media_item, definition=prop)

            if prop.type == 'text':
                property.value = value
            else:
                value = int(value)

                if value > 0:
                    enum_item = MediaItemPropertyEnumerationItem.objects.get(pk=value)
                    property.enum_item = enum_item
                else:
                    property.enum_item = 0

            property.save()

    return media_item_edit(request, media_item_id)
    
    
    

    

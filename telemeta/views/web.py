
import telemeta
from django.template import Context, loader
from django.http import HttpResponse
from django.http import Http404
from telemeta.models import MediaItem
from telemeta.models import MediaCollection
from django.shortcuts import render_to_response
import re
from telemeta.core import *
from telemeta.core import ComponentManager
from telemeta.export import *
from django.conf import settings
import os

def index(request):
    "Render the homepage"

    media_items = MediaItem.objects.all()
    template = loader.get_template('index.html')
    context = Context({
        'media_items' : media_items,
    })
    return HttpResponse(template.render(context))

class WebView(Component):

    exporters = ExtensionPoint(IExporter)

    def item_detail(self, request, item_id):
        item = MediaItem.objects.get(pk=item_id)
        formats = []
        for exporter in self.exporters:
            formats.append(exporter.get_format())
        return render_to_response('mediaitem_detail.html', 
                    {'item': item, 'export_formats': formats})

    def file_stream(self, filepath):
        buffer_size = 0xFFFF
        f = open(filepath, 'rb')
        chunk = f.read(buffer_size)
        yield chunk
        while chunk:
            chunk = f.read(buffer_size)
            yield chunk
        f.close()            

    def item_export(self, request, item_id, format):                    
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

        response = HttpResponse(self.file_stream(outfile), mimetype = mime_type)
        response['Content-Disposition'] = 'attachment; filename="download.' + \
                    exporter.get_file_extension() + '"'
        return response

    def quick_search(self, request):
        pattern = request.REQUEST["pattern"]
        collections = MediaCollection.objects.quick_search(pattern)
        items = MediaItem.objects.quick_search(pattern)
        return render_to_response('search_results.html', 
                    {'pattern': pattern, 'collections': collections, 
                     'items': items})

        

comp_mgr = ComponentManager()
view = WebView(comp_mgr)
item_detail = view.item_detail
item_export = view.item_export
quick_search = view.quick_search

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
    
    
    

    

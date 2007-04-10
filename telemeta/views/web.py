
import telemeta
from django.template import Context, loader
from django.http import HttpResponse
from telemeta.models import MediaItem
from telemeta.models import MediaItemPropertyDefinition
from telemeta.models import MediaItemPropertyEnumerationItem
from telemeta.models import MediaItemProperty
from django.shortcuts import render_to_response
import re

def index(request):
    "Render the homepage"

    media_items = MediaItem.objects.all()
    template = loader.get_template('index.html')
    context = Context({
        'media_items' : media_items,
    })
    return HttpResponse(template.render(context))

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
    
    
    

    

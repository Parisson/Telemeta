from optparse import make_option
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.core.files.base import ContentFile
from telemeta.models import *
from telemeta.util.unaccent import unaccent
from telemeta.util.url import URLMediaParser
import os


class Command(BaseCommand):
    help = "import media files from a URL directory into a collection with a given prefix"
    args = "collection_code URL"

    def handle(self, *args, **options):
        collection_code = args[0]
        prefix = args[1]
        url = args[2]

        parser = URLMediaParser(url)
        urls = parser.get_urls()
        collections = MediaCollection.objects.filter(code=collection_code)
        if not collections:
            collection = MediaCollection(code=collection_code, title=collection_code)
            collection.public_access = 'full'
            collection.save()
            print 'collection created: ' + collection_code
        else:
            collection = collections[0]
            print 'using collection: ' + collection.code

        for url in urls:
            filename = url.split('/')[-1]
            name, ext = os.path.splitext(filename)
            items = MediaItem.objects.filter(code=name)
            if not items and prefix in name:
                code = collection.code + '_' + name
                item = MediaItem(collection=collection, code=code)
                item.title = name
                item.url = url
                item.public_access = 'full'
                item.save()
                print 'item created: ' + item.code
            else:
                print 'item already exists: ' + items[0].code

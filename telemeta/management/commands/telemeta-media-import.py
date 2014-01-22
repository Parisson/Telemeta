from optparse import make_option
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.core.files.base import ContentFile
from telemeta.models import *
from telemeta.util.unaccent import unaccent
from telemeta.cache import TelemetaCache
import urllib

try:
    from django.utils.text import slugify
except ImportError:
    def slugify(string):
        killed_chars = re.sub('[\(\),]', '', string)
        return re.sub(' ', '_', killed_chars)

def beautify(string):
    return os.path.splitext(string)[0].replace('_',' ')

class Command(BaseCommand):
    args = "<media_file1 [media_file2 ...]>"
    help = "Download and import a media item"
    option_list = BaseCommand.option_list + (
            make_option('--collection-code',
                action='store',
                dest='code',
                default='default',
                metavar = '<code>',
                help='collection code'),
            make_option('--collection-title',
                action='store',
                dest='title',
                default='default',
                metavar = '<title>',
                help='collection title'),
            )

    cache_data = TelemetaCache(settings.TELEMETA_DATA_CACHE_DIR)
    cache_export = TelemetaCache(settings.TELEMETA_EXPORT_CACHE_DIR)

    urls = []

    def handle(self, *args, **options):
        if len(args) < 1:
            return
        if options['title']: 
            self.title = options['title']
        if options['code']: 
            self.code = options['code']
        for file in args:
            self.urls.append('file://' + file)

        collections = MediaCollection.objects.filter(code=self.code)
        if not collections:
            # create a new collection
            collection = MediaCollection(code=self.code, title=self.title)
            collection.public_access = 'full'
            collection.save()
        else:
            collection = collections[0]

        for url in self.urls:
            basename = os.path.basename(url)
            code = slugify(basename)
            title = beautify(basename)
            items = MediaItem.objects.filter(code=code)
            if not items:
                item = MediaItem(collection=collection, code=code, title=title)
                item.save()
            else:
                print 'cleaning up', code
                item = items[0]
                self.cache_data.delete_item_data(code)
                self.cache_export.delete_item_data(code)
                flags = MediaItemTranscodingFlag.objects.filter(item=item)
                analyses = MediaItemAnalysis.objects.filter(item=item)
                for flag in flags:
                    flag.delete()
                for analysis in analyses:
                    analysis.delete()

            print 'fetching: ' + url
            file = urllib.urlopen(url)
            file_content = ContentFile(file.read())
            item.title = title
            item.file.save(code, file_content)
            item.public_access = 'full'
            item.save()
            print 'item created: ', collection, code

        print 'done importing', len(self.urls), 'items'

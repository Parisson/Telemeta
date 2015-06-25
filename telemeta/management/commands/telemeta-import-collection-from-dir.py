from optparse import make_option
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.core.files.base import ContentFile
from django.contrib.auth.models import User
from telemeta.models import *
from telemeta.util.unaccent import unaccent
import os


try:
    from django.utils.text import slugify
except ImportError:
    def slugify(string):
        killed_chars = re.sub('[\(\),]', '', string)
        return re.sub(' ', '_', killed_chars)

def beautify(string):
    return os.path.splitext(string)[0].replace('_',' ')


class Command(BaseCommand):
    help = "import media files from a directory into a collection"
    media_root = os.path.normpath(settings.MEDIA_ROOT)

    option_list = BaseCommand.option_list + (
            make_option('-d', '--dry-run',
                action='store_true',
                dest='dry-run',
                help='Do NOT write anything'),
            make_option('-f', '--force',
                action='store_true',
                dest='force',
                help='Force overwrite data'),
            make_option('-s', '--source',
                dest='source_dir',
                help='define the source directory'),
            make_option('-l', '--log',
                dest='log',
                help='define log file'),
            make_option('-p', '--pattern',
                dest='pattern',
                help='define the pattern'),
            make_option('-u', '--username',
                dest='user',
                help='define the username'),
            make_option('-c', '--collection-code',
                action='store',
                dest='collection_code',
                default='default',
                metavar = '<code>',
                help='collection code'),
            make_option('-t', '--collection-title',
                action='store',
                dest='collection_title',
                default='default',
                metavar = '<title>',
                help='collection title'),

    )

    def write_file(self, item, media):
        filename = media.split(os.sep)[-1]
        if os.path.exists(media):
            if not item.file or self.force:
                if not self.media_root in self.source_dir:
                    print "file not in MEDIA_ROOT, copying..."
                    f = open(media, 'r')
                    if not self.dry_run:
                        file_content = ContentFile(f.read())
                        item.file.save(filename, file_content)
                        item.save()
                    f.close()
                else:
                    print "file in MEDIA_ROOT, linking..."
                    path = media[len(self.media_root)+1:]
                    if not self.dry_run:
                        item.file = path
                        item.save()
                if self.user:
                    item.set_revision(self.user)

    def handle(self, *args, **options):
        self.source_dir = os.path.abspath(options.get('source_dir'))
        self.collection_code = options.get('collection_code')
        self.collection_title = options.get('collection_title')
        self.dry_run = options.get('dry-run')
        self.user = None
        self.pattern = options.get('pattern')
        self.force = options.get('force')

        users = User.objects.filter(username=options.get('username'))
        if users:
            self.user = users[0]

        collection, c = MediaCollection.objects.get_or_create(code=self.collection_code, title=self.collection_code)
        if c:
            collection.public_access = 'full'
            collection.save()
            print 'Collection created: ' + self.collection_code
        else:
            print 'Using collection: ' + collection.code

        for root, dirs, files in os.walk(self.source_dir):
            for filename in files:
                path = root + os.sep + filename
                filename_pre, ext = os.path.splitext(filename)
                item_code = collection.code + '_' + filename_pre
                item, c = MediaItem.objects.get_or_create(collection=collection, code=item_code)
                if c:
                    item.title = filename_pre
                    item.public_access = 'full'
                    self.write_file(item, path)
                    item.save()
                    print 'item created: ' + item.code
                else:
                    print 'item already exists: ' + item.code

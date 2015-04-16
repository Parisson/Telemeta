from optparse import make_option
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.core.files.base import ContentFile
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

def remove_dir_spaces(root_dir):
    for resource in os.listdir(root_dir):
        path = os.path.join(root_dir, resource)
        if os.path.isdir(path):
            new_path = path.replace(' ', '_')
            if new_path != path:
                os.rename(path, new_path)
            remove_dir_spaces(new_path)

def trim_list(list):
    new = []
    for item in list:
        if item:
            new.append(item)
    return new

class Command(BaseCommand):
    help = "import media files from a directory to a corpus"
    args = "root_dir"
    media_formats = ['mp3']
    image_formats = ['png', 'jpg']
    text_formats = ['txt']

    def handle(self, *args, **options):
        root_dir = args[-1]
        remove_dir_spaces(root_dir)

        for root, dirs, files in os.walk(root_dir):
            for media_file in files:
                path = os.path.join(root, media_file)

                if ' ' in media_file:
                    new_media_file = media_file.replace(' ', '_')
                    new_media_path = os.path.join(root, new_media_file)
                    os.rename(path, new_media_path)
                    media_file = new_media_file
                    print media_file

                media_name = os.path.splitext(media_file)[0]
                media_ext = os.path.splitext(media_file)[1][1:]

                if media_ext and media_ext in self.media_formats and media_name[0] != '.':
                    root_list = root.split(os.sep)
                    media_path = os.sep.join(root_list[-4:])  + os.sep + media_file

                    item_name = root_list[-1]
                    collection_name = root_list[-2]
                    corpus_name = root_list[-3]

                    corpus_id = slugify(unicode(corpus_name))
                    collection_id = corpus_id + '_' + slugify(unicode(collection_name))
                    item_id = collection_id + '_' + slugify(unicode(item_name))

                    corpus, c = MediaCorpus.objects.get_or_create(code=corpus_id, title=corpus_name)

                    collection, c = MediaCollection.objects.get_or_create(code=collection_id, title=collection_name)
                    if not collection in corpus.children.all():
                        corpus.children.add(collection)

                    item, c = MediaItem.objects.get_or_create(collection=collection, code=item_id)
                    if c:
                        item.old_code = item_name
                        item.file = media_path
                        item.save()

                        for related_file in os.listdir(root):
                            related_path = root + os.sep + related_file
                            related_ext = os.path.splitext(related_file)[1][1:]
                            if related_ext in self.text_formats:
                                text = open(related_path, 'r')
                                lines = trim_list(text.read().splitlines())
                                print lines
                                break

                        if lines:
                             item.track = lines[2]
                             item.title = lines[3][:255]
                             item.save()

                        for related_file in os.listdir(root):
                            related_path = os.sep.join(root_list[-4:]) + os.sep + related_file
                            related_name = os.path.splitext(related_file)[0]
                            related_ext = os.path.splitext(related_file)[1][1:]

                            print related_path
                            if related_ext in self.image_formats:
                                related, c = MediaItemRelated.objects.get_or_create(item=item, file=related_path)
                                if c:
                                    if lines:
                                        related.title = lines[4]
                                    related.set_mime_type()
                                    related.save()


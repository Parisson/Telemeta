from optparse import make_option
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.core.files.base import ContentFile
from telemeta.models import *
from telemeta.util.unaccent import unaccent
import os, re

try:
    from django.utils.text import slugify
except ImportError:
    def slugify(string):
        killed_chars = re.sub('[\(\),]', '', string)
        return re.sub(' ', '_', killed_chars)

def beautify(string):
    return os.path.splitext(string)[0].replace('_',' ')

def cleanup_dir(root_dir):
    for resource in os.listdir(root_dir):
        path = os.path.join(root_dir, resource)
        if os.path.isdir(path):
            new_path = path.replace(' ', '_')
            new_path = new_path.replace('son_', '')
            new_path = new_path.replace('son', '')
            if new_path != path:
                os.rename(path, new_path)
            cleanup_dir(new_path)

def trim_list(list):
    new = []
    for item in list:
        if item:
            new.append(item)
    return new

def reset():
    for i in MediaItem.objects.all():
        i.delete()
    for c in MediaCollection.objects.all():
        c.delete()


class Command(BaseCommand):
    help = "import media files from a directory to a corpus"
    args = "root_dir"
    media_formats = ['mp3']
    image_formats = ['png', 'jpg']
    text_formats = ['txt']

    def handle(self, *args, **options):
        # NOT4PROD!!
        reset()

        root_dir = args[-1]
        cleanup_dir(root_dir)
        chapters = os.listdir(root_dir)

        for chapter in chapters:
            chapter_dir = os.path.join(root_dir, chapter)
            metadata = {}

            for filename in os.listdir(chapter_dir):
                path = os.path.join(chapter_dir, filename)
                if os.path.isfile(path) and '.txt' == os.path.splitext(filename)[1]:
                    f = open(path, 'r')
                    for line in f.readlines():
                        data = re.split(r'\t+', line.rstrip('\t'))
                        metadata[data[0]] = data[1:]
                    print metadata
                    break

            for root, dirs, files in os.walk(chapter_dir):
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
                        data = metadata[item_name]

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
                            # item.track = item_name
                            item.file = media_path
                            item.save()

                            title = data[1].split('.')
                            item.title = title[0]
                            item.track = data[2].replace('\n', '')
                            if len(title) > 1:
                                 item.comment = '. '.join(title[1:])
                            item.save()

                            for related_file in os.listdir(root):
                                related_path = os.sep.join(root_list[-4:]) + os.sep + related_file
                                related_name = os.path.splitext(related_file)[0]
                                related_ext = os.path.splitext(related_file)[1][1:]

                                if related_ext in self.image_formats:
                                    related, c = MediaItemRelated.objects.get_or_create(item=item, file=related_path)
                                    if c:
                                        if len(data) > 2:
                                            related.title = item.track
                                        related.set_mime_type()
                                        related.save()


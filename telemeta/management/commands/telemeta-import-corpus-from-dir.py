from optparse import make_option
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.core.files.base import ContentFile
from django.contrib.auth.models import User
from telemeta.models import *
from telemeta.util.unaccent import unaccent
import os, re, glob

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
    media_root = settings.MEDIA_ROOT
    dry_run = False
    user = User.objects.get(username='admin')

    def write_file(self, item, media):
        filename = media.split(os.sep)[-1]
        print media
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
                    path = media.replace(self.media_root, '')
                    if not self.dry_run:
                        item.file = path
                        item.save()
                if self.user:
                    item.set_revision(self.user)

    def handle(self, *args, **options):
        # NOT4PROD!!
        reset()

        root_dir = args[-1]
        self.source_dir = root_dir
        print self.source_dir
        print self.media_root
        cleanup_dir(self.source_dir)
        chapters = os.listdir(self.source_dir)
        corpus_name = os.path.split(root_dir)[-1]
        corpus_id = slugify(unicode(corpus_name))

        cc = MediaCorpus.objects.filter(code=corpus_id)
        if cc:
            corpus = cc[0]
        else:
            corpus = MediaCorpus(code=corpus_id)
            corpus.title = corpus_name
            corpus.save()

        for chapter in chapters:
            chapter_dir = os.path.join(self.source_dir, chapter)
            metadata = {}

            for filename in os.listdir(chapter_dir):
                path = os.path.join(chapter_dir, filename)
                if os.path.isfile(path) and '.txt' == os.path.splitext(filename)[1]:
                    f = open(path, 'r')
                    i = 0
                    for line in f.readlines():
                        data = re.split(r'\t+', line.rstrip('\t'))
                        if i == 0:
                            chapter_title = data[1]
                            print chapter_title
                        else:
                            metadata[data[0]] = data[1:]
                        i += 1
                    print metadata

            collection_name = chapter
            collection_id = corpus_id + '_' + slugify(unicode(collection_name))
            collection_title = collection_name.replace('_', ' ') + ' - ' + chapter_title
            print collection_title
            cc = MediaCollection.objects.filter(code=collection_id, title=collection_title)
            if cc:
                collection = cc[0]
            else:
                collection = MediaCollection(code=collection_id)
                collection.title = collection_title
                collection.save()
            if not collection in corpus.children.all():
                corpus.children.add(collection)

            for filename in os.listdir(chapter_dir):
                path = os.path.join(chapter_dir, filename)
                if os.path.isfile(path) and '.jpg' == os.path.splitext(filename)[1]:
                    related_path = path.replace(self.media_root, '')
                    related, c = MediaCollectionRelated.objects.get_or_create(collection=collection,
                                    file=related_path)

            for root, dirs, files in os.walk(chapter_dir):
                for media_file in files:
                    path = os.path.join(root, media_file)
                    print path
                    new_media_file = slugify(unicode(media_file.decode('utf8')))
                    if new_media_file[-3] != '.':
                        new_media_file = new_media_file[:-3] + '.' + new_media_file[-3:]
                    print new_media_file
                    if new_media_file != media_file:
                        new_media_path = os.path.join(root, new_media_file)
                        os.rename(path, new_media_path)
                        media_file = new_media_file
                        print 'renaming: ' + media_file
                        path = new_media_path

                    media_name = os.path.splitext(media_file)[0]
                    media_ext = os.path.splitext(media_file)[1][1:]

                    if media_ext and media_ext in self.media_formats and media_name[0] != '.':
                        root_list = root.split(os.sep)
                        media_path = os.sep.join(root_list[-4:])  + os.sep + media_file
                        item_name = root_list[-1]
                        item_id = collection_id + '_' + slugify(unicode(item_name))
                        data = metadata[item_name]
                        item, c = MediaItem.objects.get_or_create(collection=collection, code=item_id)
                        item.old_code = item_name
                        self.write_file(item, path)
                        title = data[0].split('.')
                        item.title = title[0].replace('\n', '')
                        print data
                        if len(data) > 1:
                            item.track = data[1].replace('\n', '')
                        if len(title) > 1:
                            item.comment = '. '.join(title[1:])
                        item.save()
                        for related_file in os.listdir(root):
                            related_path = os.sep.join(root_list[-4:]) + os.sep + related_file
                            related_name = os.path.splitext(related_file)[0]
                            related_ext = os.path.splitext(related_file)[1][1:]
                            if related_ext in self.image_formats:
                                related, c = MediaItemRelated.objects.get_or_create(item=item, file=related_path)
                                if len(data) > 2:
                                    related.title = item.track
                                related.set_mime_type()
                                related.save()


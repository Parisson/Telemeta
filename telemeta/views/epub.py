# -*- coding: utf-8 -*-
# Copyright (C) 2015 Parisson SARL

# This software is a computer program whose purpose is to backup, analyse,
# transcode and stream any audio content with its metadata over a web frontend.

# This software is governed by the CeCILL  license under French law and
# abiding by the rules of distribution of free software.  You can  use,
# modify and/ or redistribute the software under the terms of the CeCILL
# license as circulated by CEA, CNRS and INRIA at the following URL
# "http://www.cecill.info".

# As a counterpart to the access to the source code and  rights to copy,
# modify and redistribute granted by the license, users are provided only
# with a limited warranty  and the software's author,  the holder of the
# economic rights,  and the successive licensors  have only  limited
# liability.

# In this respect, the user's attention is drawn to the risks associated
# with loading,  using,  modifying and/or developing or reproducing the
# software by the user in light of its specific status of free software,
# that may mean  that it is complicated to manipulate,  and  that  also
# therefore means  that it is reserved for developers  and  experienced
# professionals having in-depth computer knowledge. Users are therefore
# encouraged to load and test the software's suitability as regards their
# requirements in conditions enabling the security of their systems and/or
# data to be ensured and,  more generally, to use and operate it in the
# same conditions as regards security.

# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL license and that you accept its terms.

# Authors: Guillaume Pellerin <yomguy@parisson.com>


from telemeta.views.core import *
from telemeta.models import *
from collections import OrderedDict
from ebooklib import epub
from django.template.loader import render_to_string


class BaseEpubMixin(TelemetaBaseMixin):
    "Download corpus data embedded in an EPUB3 file"

    local_path = os.path.dirname(__file__)
    css = os.sep.join([local_path, '..', 'static', 'telemeta', 'css', 'telemeta_epub.css'])
    default_image = os.sep.join([local_path, '..', 'static', 'telemeta', 'images', 'cul_de_lampe.jpg'])
    template = os.sep.join([local_path, '..', 'templates', 'telemeta', 'inc', 'epub_collection.html'])
    template_preamble = os.sep.join([local_path, '..', 'templates', 'telemeta', 'inc', 'epub_preamble.html'])

    def write_book(self, corpus, collection=None, path=None):
        self.book = epub.EpubBook()
        self.corpus = corpus
        site = Site.objects.get_current()
        self.chapters = []
        default_image_added = False

        if not collection:
            self.filename = self.corpus.code
            self.book.set_title(corpus.title)
        else:
            self.filename = collection.code
            self.book.set_title(corpus.title + ' - ' + collection.title)

        self.path = self.cache_data.dir + os.sep + self.filename + '.epub'

        # add metadata
        self.book.set_identifier(corpus.public_id)
        self.book.set_language('fr')
        self.book.add_author(corpus.descriptions)

        # add css style
        style = open(self.css, 'r')
        css = epub.EpubItem(uid="style_nav", file_name="style/epub.css", media_type="text/css", content=style.read())
        self.book.add_item(css)

        if collection:
            self.collections = [collection]
            mode_single = True
            instance = collection
        else:
            self.collections = self.corpus.children.all()
            mode_single = False
            instance = self.corpus

        # add cover image
        for media in instance.related.all():
            filename = os.path.split(media.file.path)[-1]
            self.book.set_cover(filename, open(media.file.path, 'r').read())
            break

        context = {}
        preamble = epub.EpubHtml(title='Preamble', file_name='preamble' + '.xhtml', lang='fr')
        preamble.content = render_to_string(self.template_preamble, context)
        preamble.is_chapter = False
        self.book.add_item(preamble)
        self.chapters.append(preamble)

        for collection in self.collections:
            items = {}
            default_image_added = False
            default_image_relative_path = ''

            for item in collection.items.all():
                if '.' in item.old_code:
                    id = item.old_code.split('.')[1]
                else:
                    id = item.old_code
                for c in id:
                    if c.isalpha():
                        id = id.replace(c, '.' + str(ord(c)-96))
                items[item] = float(id)
            items = OrderedDict(sorted(items.items(), key=lambda t: t[1]))

            for item in items:
                if item.file:
                    audio = open(item.file.path, 'r')
                    filename = str(item.file)
                    epub_item = epub.EpubItem(file_name=str(item.file), content=audio.read())
                    self.book.add_item(epub_item)

                related_all = item.related.all()
                if related_all:
                    for related in related_all:
                        if 'image' in related.mime_type:
                            image = open(related.file.path, 'r')
                            epub_item = epub.EpubItem(file_name=str(related.file), content=image.read())
                            self.book.add_item(epub_item)
                elif not default_image_added:
                    image = open(self.default_image, 'r')
                    default_image_relative_path = 'images' + os.sep + os.path.split(self.default_image)[-1]
                    epub_item = epub.EpubItem(file_name=default_image_relative_path,
                                        content=image.read())
                    self.book.add_item(epub_item)
                    default_image_added = True


            title_split = collection.title.split(' - ')
            if len(title_split) > 1:
                if '0' in title_split[0]:
                    title = title_split[1]
                    subtitle = ''
                else:
                    title = title_split[0]
                    subtitle = title_split[1]
            else:
                title = collection.title
                subtitle = ''

            context = {'collection': collection, 'title': title, 'subtitle': subtitle,
                        'site': site, 'items': items, 'default_image': default_image_relative_path}
            c = epub.EpubHtml(title=' - '.join([title, subtitle]), file_name=collection.code + '.xhtml', lang='fr')
            c.content = render_to_string(self.template, context)
            self.chapters.append(c)
            # add self.chapters to the self.book
            self.book.add_item(c)

        # create table of contents
        # - add manual link
        # - add section
        # - add auto created links to chapters
        self.book.toc = (( self.chapters ))

        # add navigation files
        self.book.add_item(epub.EpubNcx())
        if not mode_single:
            self.book.add_item(epub.EpubNav())
            self.chapters.insert(0,'nav')

        # create spin, add cover page as first page
        self.chapters.insert(0,'cover')
        self.book.spine = self.chapters

        # write epub file
        epub.write_epub(self.path, self.book, {})


class CorpusEpubView(BaseEpubMixin, View):
    "Download corpus data embedded in an EPUB3 file"

    model = MediaCorpus

    def get_object(self):
        return MediaCorpus.objects.get(public_id=self.kwargs['public_id'])

    def get(self, request, *args, **kwargs):
        self.write_book(self.get_object())
        epub_file = open(self.path, 'rb')
        response = HttpResponse(epub_file.read(), content_type='application/epub+zip')
        response['Content-Disposition'] = "attachment; filename=%s" % self.filename + '.epub'
        return response

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(CorpusEpubView, self).dispatch(*args, **kwargs)



class CollectionEpubView(BaseEpubMixin, View):
    "Download collection data embedded in an EPUB3 file"

    model = MediaCollection

    def get_object(self):
        return MediaCollection.objects.get(public_id=self.kwargs['public_id'])

    def get(self, request, *args, **kwargs):
        collection = self.get_object()
        corpus = collection.corpus.all()[0]
        self.write_book(corpus, collection=collection)
        epub_file = open(self.path, 'rb')
        response = HttpResponse(epub_file.read(), content_type='application/epub+zip')
        response['Content-Disposition'] = "attachment; filename=%s" % self.filename + '.epub'
        return response

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(CollectionEpubView, self).dispatch(*args, **kwargs)


# -*- coding: utf-8 -*-
# Copyright (C) 2015-2017 Parisson SARL

# This file is part of Telemeta.

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# Authors: Guillaume Pellerin <yomguy@parisson.com>


from telemeta.views.core import TelemetaBaseMixin
from telemeta.models import Site
from collections import OrderedDict
from ebooklib import epub
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _

import os


class BaseEpubMixin(TelemetaBaseMixin):
    "Download corpus data embedded in an EPUB3 file"

    local_path = os.path.dirname(__file__)
    css = os.sep.join([local_path, '..', 'static', 'telemeta', 'css', 'telemeta_epub.css'])
    default_image = os.sep.join([local_path, '..', 'static', 'telemeta', 'images', 'cul_de_lampe.jpg'])
    default_image_end = os.sep.join([local_path, '..', 'static', 'telemeta', 'images', 'cul_de_lampe-fin_page.jpg'])
    template = os.sep.join([local_path, '..', 'templates', 'telemeta', 'inc', 'epub_collection.html'])
    template_preamble = os.sep.join([local_path, '..', 'templates', 'telemeta', 'inc', 'epub_preamble.html'])
    template_cover = os.sep.join([local_path, '..', 'templates', 'telemeta', 'inc', 'epub_cover.html'])

    def setup_epub(self, corpus, collection=None, path=None):
        self.book = epub.EpubBook()
        self.corpus = corpus
        self.collection = collection
        self.site = Site.objects.get_current()
        self.chapters = []
        self.default_image_added = False

        if not collection:
            self.filename = corpus.code
            self.book.set_title(corpus.title)
            self.full_title = corpus.title
        else:
            self.filename = collection.code
            short_title = collection.title.split(' ')
            if not ' 0' in collection.title:
                short_title = short_title[0][:4] + ' ' + short_title[1]
            else:
                short_title = 'Intro'
            self.book.set_title(corpus.title[:15] + '... ' + short_title)
            self.full_title = corpus.title + ' - ' + collection.title

        self.path = self.cache_data.dir + os.sep + self.filename + '.epub'
        return self.path

    def write_book(self):

        # add metadata
        self.book.set_identifier(self.corpus.public_id)
        self.book.set_language('fr')
        self.book.add_author(self.corpus.descriptions)

        # add css style
        style = open(self.css, 'r')
        css = epub.EpubItem(uid="style_nav", file_name="style/epub.css", media_type="text/css", content=style.read())
        self.book.add_item(css)

        if self.collection:
            self.collections = [self.collection]
            mode_single = True
            instance = self.collection
            if ' 0' in self.collection.title:
                chap_num = "d'introduction"
            else:
                chap_num = self.collection.code.split('_')[-1]
            context = {'title': 'chapitre ' + chap_num,
                       'mode_single': mode_single}
        else:
            self.collections = self.corpus.children.all()
            mode_single = False
            instance = self.corpus
            context = {'title': '', 'mode_single': mode_single}

        # add cover image
        for media in instance.related.all():
            self.cover_filename = os.path.split(media.file.path)[-1]
            self.book.set_cover(self.cover_filename, open(media.file.path, 'rb').read())
            break

        preamble = epub.EpubHtml(title='Copyright', file_name='copyright' + '.xhtml', lang='fr')
        preamble.content = render_to_string(self.template_preamble, context)
        preamble.is_chapter = True
        self.default_image_added = False
        default_image_relative_path = ''
        self.book.add_item(preamble)
        self.chapters.append(preamble)

        image = open(self.default_image_end, 'r')
        default_image_end_relative_path = 'images' + os.sep + os.path.split(self.default_image_end)[-1]
        epub_last_image = epub.EpubItem(file_name=default_image_end_relative_path,
                                        content=image.read())
        self.book.add_item(epub_last_image)
        i = 1

        for collection in self.collections:
            items = {}
            for item in collection.items.all():
                if '.' in item.old_code:
                    id = item.old_code.split('.')[1]
                else:
                    id = item.old_code
                for c in id:
                    if c.isalpha():
                        id = id.replace(c, '.' + str(ord(c) - 96))
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
                elif not self.default_image_added:
                    image = open(self.default_image, 'r')
                    default_image_relative_path = 'images' + os.sep + os.path.split(self.default_image)[-1]
                    epub_item = epub.EpubItem(file_name=default_image_relative_path,
                                              content=image.read())
                    self.book.add_item(epub_item)
                    self.default_image_added = True

            title_split = collection.title.split(' - ')
            if len(title_split) > 1:
                if ' 0' in title_split[0]:
                    title = ''
                    subtitle = title_split[1]
                    chapter_title = subtitle
                else:
                    title = title_split[0]
                    subtitle = title_split[1]
                    chapter_title = ' - '.join([title, subtitle])
            else:
                title = collection.title
                subtitle = ''
                chapter_title = title

            last_collection = False
            if i == len(self.collections):
                last_collection = True

            context = {'collection': collection, 'title': title, 'subtitle': subtitle, 'mode_single': mode_single,
                       'site': self.site, 'items': items, 'default_image': default_image_relative_path,
                       'default_image_end': default_image_end_relative_path, 'last_collection': last_collection}
            c = epub.EpubHtml(title=chapter_title, file_name=collection.code + '.xhtml', lang='fr')
            c.content = render_to_string(self.template, context)
            self.book.add_item(c)
            self.chapters.append(c)
            i += 1

        # create table of contents
        # - add manual link
        # - add section
        # - add auto created links to chapters
        self.book.toc = ((self.chapters))
        self.book.spine = self.chapters

        # add navigation files
        ncx = epub.EpubNcx()
        self.book.add_item(ncx)
        nav = epub.EpubNav()
        self.book.add_item(nav)
        if not mode_single:
            self.book.spine.insert(0, 'nav')

        # create spin, add cover page as first page
        cover = epub.EpubHtml(title=self.full_title, file_name='cover-bis' + '.xhtml')
        cover.content = render_to_string(self.template_cover, {'image': self.cover_filename})
        self.book.add_item(cover)
        self.book.spine.insert(0, cover)

        # self.book.guide.insert(0, {
        # "type"  : "cover",
        # "href"  : cover.file_name,
        # "title" : cover.title,
        # })

        # write epub file
        epub.write_epub(self.path, self.book, {})

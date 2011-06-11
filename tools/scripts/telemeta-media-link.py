#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2010 Guillaume Pellerin
# All rights reserved.
#
# This software is licensed as described in the file COPYING, which
# you should have received as part of this distribution. The terms
# are also available at http://svn.parisson.org/telemeta/TelemetaLicense.
#
# Author: Guillaume Pellerin <yomguy@parisson.com>
#

import os
import re
import sys
import logging
import datetime
import timeside
from django.utils import html
from django.core.management import setup_environ
from django.core.files.base import ContentFile


class Logger:

    def __init__(self, file):
        self.logger = logging.getLogger('myapp')
        self.hdlr = logging.FileHandler(file)
        self.formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        self.hdlr.setFormatter(self.formatter)
        self.logger.addHandler(self.hdlr)
        self.logger.setLevel(logging.INFO)

    def write_info(self, prefix, message):
        self.logger.info(' ' + prefix + ' : ' + message.decode('utf8'))

    def write_error(self, prefix, message):
        self.logger.error(prefix + ' : ' + message.decode('utf8'))


class TelemetaMediaImport:

    def __init__(self, media_dir, log_file):
        self.logger = Logger(log_file)
        self.media_dir = media_dir
        self.medias = self.get_medias()
    
    def get_medias(self):
        os.chdir(self.media_dir)
        file_list = []
        for root, dirs, files in os.walk('.'):
            for file in files:
                path = root + os.sep + file
                if not os.sep+'.' in path:
                    file_list.append({'root': root, 'file': file})
        return file_list
        
    def set_collection(self, collection_name):
        if not collection_name:
            collection_name = 'Unkown'
        code = collection_name.replace(' ','_')
        code = code.replace("'",'_')
        code = re.escape(code)
        code = code.replace("\\",'')
        code = code.replace("(",'_')
        code = code.replace(")",'_')
        code = code.replace(",",'_')
        print code
        #code = html.escape(code)
        from telemeta.models.media import MediaCollection
        collections = MediaCollection.objects.filter(code=code)
        if not collections:
            collection = MediaCollection(code=code,title=collection_name)
            collection.save()
            msg = 'created'
            self.logger.write_info('collection ' + collection_name, msg)
        else:
            collection = collections[0]
        return collection

    def media_import(self):
        from telemeta.models.media import MediaItem
        for media in self.medias:
            path = media['root'] + os.sep + media['file']
            print 'checking ' + path
            filename,  ext = os.path.splitext(media['file'])
            item = MediaItem.objects.filter(code=filename)
            if not item:
                print 'importing ' + path
                decoder = timeside.decoder.FileDecoder(path)
                obj = timeside.decoder.metadata.Mp3Metadata(path)
                metadata = obj.metadata()
                print metadata
                collection = self.set_collection(metadata['album'])
                item = MediaItem(collection=collection)
                item.title = metadata['title']
                item.author = metadata['artist']
                #item.generic_style = metadata.genre
                date = metadata['date']
                if not date or date == '0000':
                    date = '1900'
                if not len(date) > 4:
                    item.recorded_from_date = date + '-01-01'
                item.file = path
                item.save()
                msg = 'added item : ' + path
                self.logger.write_info(collection.code, msg)


def run():
    project_dir = sys.argv[-2]
    log_file = sys.argv[-1]
    sys.path.append(project_dir)
    import settings
    setup_environ(settings)
    media_dir = settings.MEDIA_ROOT
    t = TelemetaMediaImport(media_dir, log_file)
    t.media_import()

if __name__ == '__main__':
    run()

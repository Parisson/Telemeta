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
from django.core.management import setup_environ
from django.core.files.base import ContentFile

mapping = {
             'title': 'title',
             'album': 'collection',
             'date': 'recorded_from_date',
             'artist': 'author',
             'track-number': 'track',
             'encoder': 'comment',
             'genre': 'generic_style',
             'audio-codec': 'comment',
             'container-format': 'comment',
             }

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
        code = re.sub(r'\W+', '_', code)
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
                try:
                    metadata = decoder.metadata()
                    print metadata
                    collection = self.set_collection(metadata['album'])
                    item = MediaItem(collection=collection)
                    item.code = re.sub(r'\W+', '_', metadata['title'])
                    for tag in mapping.keys():
                        try:
                            if tag == 'date':
                                date = metadata[tag].split(' ')[1].split('/')
                                metadata[tag] = date[2]+'-'+date[1]+'-'+date[0]    
                            if mapping[tag] == 'comment':
                                item[mapping[tag]] = item[mapping[tag]] + '\n' + metadata[tag]
                            else:
                                item[mapping[tag]] = metadata[tag]
                        except:
                            continue
                    item.file = path
                    item.save()
                    msg = 'added item : ' + path
                    self.logger.write_info(collection.code, msg)
                except:
                    continue
                

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

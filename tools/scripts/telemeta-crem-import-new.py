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
import sys
import logging
import datetime
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


class TelemetaWavImport:

    def __init__(self, source_dir, log_file, pattern):
        self.logger = Logger(log_file)
        self.source_dir = source_dir
        self.collections = os.listdir(self.source_dir)
        self.pattern = pattern

    def wav_import(self):
        from telemeta.models import MediaItem
        for collection in self.collections:
            collection_dir = self.source_dir + os.sep + collection
            if not '/.' in collection_dir and self.pattern in collection_dir:
                self.collection_name = collection.split(os.sep)[-1]
                msg = '************************ ' + collection + ' ******************************'
                self.logger.write_info(collection, msg[:70])

                collection_files = os.listdir(collection_dir)
                for filename in collection_files:
                    wav_file = self.source_dir + os.sep + collection + os.sep + filename
                    code = filename.split('.')[0]
                    print code
                    items = MediaItem.objects.filter(code=code)
                    if len(items) != 0:
                        item = items[0]
                        print item.code + ' : id = ' + str(item.id) + " : title = " + item.title
                        if os.path.exists(wav_file):
                            if not item.file :
                                f = open(wav_file, 'r')
                                file_content = ContentFile(f.read())
                                item.file.save(filename, file_content)
                                f.close()
                                item.code = new_ref
                                item.save()
                            else:
                                msg = code + ' : fichier ' + wav_file + ' déjà ajouté !'
                                print msg
                                self.logger.write_error(collection, msg)
                        else:
                            msg = code + ' : fichier audio ' + wav_file + ' inexistant !'
                            print msg
                            self.logger.write_error(collection, msg)
                    else:
                        msg = code + ' : item inexistant dans la base de données !'
                        print msg
                        self.logger.write_error(collection, msg)


def print_usage(tool_name):
    print "Usage: "+tool_name+" <project_dir> <source_dir> <pattern> <log_file>"
    print "  project_dir: the directory of the Django project which hosts Telemeta"
    print "  source_dir: the directory containing the wav files to include"
    print "  pattern: a pattern to match the collection names"
    print "  log_file: a log file to write logs"

def run():
    if len(sys.argv) < 3:
        print_usage(os.path.basename(sys.argv[0]))
        sys.exit(1)
    else:
        project_dir = sys.argv[-4]
        source_dir = sys.argv[-3]
        pattern = sys.argv[-2]
        log_file = sys.argv[-1]
        sys.path.append(project_dir)
        import settings
        setup_environ(settings)
        t = TelemetaWavImport(source_dir, log_file, pattern)
        t.wav_import()

if __name__ == '__main__':
    run()

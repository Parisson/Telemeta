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
import csv
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

    def info(self, prefix, message):
        self.logger.info(' ' + prefix + ' : ' + message.decode('utf8'))

    def error(self, prefix, message):
        self.logger.error(prefix + ' : ' + message.decode('utf8'))


class TelemetaWavImport:

    def __init__(self, source_dir, log_file, pattern, domain):
        from django.contrib.auth.models import User
        self.logger = Logger(log_file)
        self.source_dir = source_dir
        self.collections = os.listdir(self.source_dir)
        self.pattern = pattern
        self.user = User.objects.filter(username='admin')[0]
        self.domain = domain

    def write_file(self, item, wav_file, overwrite=False):
        filename = wav_file.split(os.sep)[-1]
        if os.path.exists(wav_file):
            if not item.file or overwrite:
                f = open(wav_file, 'r')
                file_content = ContentFile(f.read())
                item.file.save(filename, file_content)
                f.close()
                item.save()
                item.set_revision(self.user)
            else:
                msg = item.code + ' : fichier ' + item.file.name + ' deja inscrit dans la base de donnees !'
                self.logger.error('item', msg)
        else:
            msg = item.code + ' : fichier audio ' + filename + ' inexistant dans le dossier !'
            self.logger.error('item', msg)

    def wav_import(self):
        from telemeta.models import MediaItem,  MediaCollection

        collections = []
        for collection in self.collections:
            collection_dir = self.source_dir + os.sep + collection
            collection_files = os.listdir(collection_dir)


            if not '/.' in collection_dir and self.pattern in collection_dir:
                collection_name = collection.split(os.sep)[-1]
                collections.append(collection_name)
                c = MediaCollection.objects.filter(code=collection_name)

                if not c and collection + '.csv' in collection_files:
                    msg = collection + ' collection NON présente dans la base de données, SORTIE '
                    self.logger.error(collection, msg)
                    sys.exit(msg)
                elif not c:
                    msg = 'collection NON présente dans la base de données, CREATION '
                    self.logger.info(collection, msg)
                    c = MediaCollection(code=collection_name, title=collection_name)
                    c.save()
                    c.set_revision(self.user)
                else:
                    msg = 'collection présente dans la base de données, SELECTION'
                    self.logger.info(collection, msg)

        for collection in collections:
            collection_dir = self.source_dir + os.sep + collection
            collection_name = collection
            collection_files = os.listdir(collection_dir)
            msg = '************************ ' + collection + ' ******************************'
            self.logger.info(collection, msg[:70])
            overwrite = True
            csv_file = ''
            rows = {}

            if collection + '.csv' in collection_files:
                csv_file = self.source_dir + os.sep + collection + os.sep + collection + '.csv'
                csv_data = csv.reader(open(csv_file), delimiter=';')
                for row in csv_data:
                    rows[row[1].strip()] = row[0].strip()
                msg = collection + ' import du fichier CSV de la collection'
                self.logger.info(collection, msg[:70])
            else:
                msg = collection + ' pas de fichier CSV dans la collection'
                self.logger.info(collection, msg[:70])

            c = MediaCollection.objects.filter(code=collection_name)
            if not c:
                c = MediaCollection(code=collection_name)
                c.save()
                msg = ' collection NON présente dans la BDD, CREATION '
                self.logger.info(c.code, msg)
            else:
                c = c[0]
                msg = ' id = '+str(c.id)
                self.logger.info(c.code, msg)

            audio_files = []
            for file in collection_files:
                ext = ['WAV', 'wav']
                if file.split('.')[-1] in ext and file[0] != '.':
                    audio_files.append(file)

            audio_files.sort()
            nb_items = c.items.count()
            counter = 0

            for file in audio_files:
                code = file.split('.')[0]
                wav_file = self.source_dir + os.sep + collection + os.sep + file

                if len(audio_files) <= nb_items:
                    items = MediaItem.objects.filter(code=code)

                    old_ref = ''
                    if code in rows and not items:
                        old_ref = rows[code]
                        items = MediaItem.objects.filter(old_code=old_ref)

                    if items:
                        item = items[0]
                        msg = code + ' : ' + item.old_code + ' : Cas 1 ou 2 : id = ' + str(item.id)
                        self.logger.info('item', msg)
                        item.code = code
                        item.save()
                    else:
                        item = MediaItem(code=code, collection=c)
                        msg = code + ' : ' + old_ref + ' : Cas 1 ou 2 : item NON présent dans la base de données, CREATION'
                        self.logger.info('item', msg)

                    self.write_file(item, wav_file, overwrite)

                elif nb_items == 1 and len(audio_files) > 1:
                    if counter == 0:
                        msg = code + ' : Cas 3a : item n°01 présent dans la base de données, PASSE'
                        self.logger.info('item', msg)
                    else:
                        item = MediaItem(code=code, collection=c)
                        msg = code + ' : Cas 3a : item NON présent dans la base de données, CREATION'
                        self.logger.info('item', msg)
                        self.write_file(item, wav_file, overwrite)

                elif nb_items > 1 and nb_items < len(audio_files):
                    msg = code + ' : Cas 3b : nb items < nb de fichiers audio, PAS de creation'
                    self.logger.info('item', msg)

                counter += 1

        msg = 'Liste des URLs des collections importées :'
        self.logger.info('INFO', msg)
        for collection in collections:
            msg = 'http://'+self.domain+'/archives/collections/'+collection
            self.logger.info(collection, msg)


def print_usage(tool_name):
    print "Usage: "+tool_name+" <project_dir> <source_dir> <pattern> <log_file> <domain>"
    print "  project_dir: the directory of the Django project which hosts Telemeta"
    print "  source_dir: the directory containing the wav files to include"
    print "  pattern: a pattern to match the collection names"
    print "  log_file: a log file to write logs"
    print "  domain: root domain for collections"

def run():
    if len(sys.argv) < 3:
        print_usage(os.path.basename(sys.argv[0]))
        sys.exit(1)
    else:
        project_dir = sys.argv[-5]
        source_dir = sys.argv[-4]
        pattern = sys.argv[-3]
        log_file = sys.argv[-2]
        url = sys.argv[-1]
        sys.path.append(project_dir)
        import settings
        setup_environ(settings)
        t = TelemetaWavImport(source_dir, log_file, pattern, url)
        t.wav_import()

if __name__ == '__main__':
    run()

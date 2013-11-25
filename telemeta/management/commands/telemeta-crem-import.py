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

import logging
import codecs
import os
import sys
import csv
import logging
import datetime
from optparse import make_option

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.core.management import setup_environ
from django.core.files.base import ContentFile
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.template.defaultfilters import slugify

from telemeta.models import *
from telemeta.util.unaccent import unaccent


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


class Command(BaseCommand):
    
    """Import CREM collections from collection directories containing media files 
    and eventually a XLS files representing the relation between old codes and new codes
    """

    help = "import CREM collections"
    args = 'source_dir pattern log_file'
    admin_email = 'webmaster@parisson.com'

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
    )


    def write_file(self, item, media):
        filename = media.split(os.sep)[-1]
        if os.path.exists(media):
            if not item.file or self.force:
                if not self.dry_run:
                    f = open(media, 'r')
                    file_content = ContentFile(f.read())
                    item.file.save(filename, file_content)
                    f.close()
                    item.save()
                    item.set_revision(self.user)
                else:
                    msg = item.code + " : pas d'écriture, utiliser l'option --write "
                    self.logger.info('item', msg)
            else:
                msg = item.code + ' : fichier ' + item.file.name + ' deja inscrit dans la base de donnees et pas de forcage !'
                self.logger.info('item', msg)
        else:
            msg = item.code + ' : fichier audio ' + filename + ' inexistant dans le dossier !'
            self.logger.error('item', msg)

    def handle(self, *args, **kwargs):
        self.logger = Logger(kwargs.get('log'))
        self.pattern = kwargs.get('pattern')
        self.source_dir = kwargs.get('source_dir')
        self.dry_run =  kwargs.get('dry-run')
        self.force = kwargs.get('force')

        self.domain = Site.objects.all()[0].domain
        self.user = User.objects.filter(username='admin')[0]
        self.collections = os.listdir(self.source_dir)
        
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
                    if not self.dry_run:
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
                if not self.dry_run:
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
                    else:
                        item = MediaItem(code=code, collection=c)
                        msg = code + ' : ' + old_ref + ' : Cas 1 ou 2 : item NON présent dans la base de données, CREATION'
                        self.logger.info('item', msg)

                    self.write_file(item, wav_file)

                elif nb_items == 1 and len(audio_files) > 1:
                    if counter == 0:
                        msg = code + ' : Cas 3a : item n°01 présent dans la base de données, PASSE'
                        self.logger.info('item', msg)
                    else:
                        item = MediaItem(code=code, collection=c)
                        msg = code + ' : Cas 3a : item NON présent dans la base de données, CREATION'
                        self.logger.info('item', msg)
                        self.write_file(item, wav_file)

                elif nb_items > 1 and nb_items < len(audio_files):
                    msg = code + ' : Cas 3b : nb items < nb de fichiers audio, PAS de creation'
                    self.logger.info('item', msg)

                counter += 1

        msg = 'Liste des URLs des collections importées :'
        self.logger.info('INFO', msg)
        for collection in collections:
            msg = 'http://'+self.domain+'/archives/collections/'+collection
            self.logger.info(collection, msg)



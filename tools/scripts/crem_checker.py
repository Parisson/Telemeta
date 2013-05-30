#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Vérifier que les nouvelles cotes d'item :

- correspondent toutes à la collection décrite par le fichier .csv
  (le fichier .csv est nommé d'après la nouvelle cote de collection)

- sont uniques dans le fichiers .csv

- ont un des formats suivant :
    - soit CNRSMH_I_aaaa_nnn_mmm
    - soit CNRSMH_I_aaaa_nnn_mmm_tt
    - soit CNRSMH_I_aaaa_nnn_mmm_tt_pp
    - soit CNRSMH_E_aaaa_nnn_mmm_tt
    - soit CNRSMH_E_aaaa_nnn_mmm_tt_pp

- correspondent à fichier .wav (et qu'il n'y a pas de fichiers .wav
  supplémentaire)

Vérifier que le répertoire est nommé d'apprès la nouvelle cote de collection

Vérifier que la nouvelle cote de collection a l'un des formats suivant :
    - soit CNRSMH_I_aaaa_nnn
    - soit CNRSMH_E_aaaa_nnn_mmm

Vérifier que les fichiers .wav sont lisibles, ont une durée et sont identifés
comme WAV par audiolab.
"""


import os
import re
import sys
import csv
import xlrd
import datetime
import logging
import shutil

COLLECTION_OLD_PATTERN = [
        { 'format': 'BM.aaa.nnn.mmm',           'regex': r'^(BM)\.([0-9]{3})\.([0-9]{3})\.([0-9]{3})$'},
        { 'format': 'BM.aaaa.nnn.mmm/pp',       'regex': r'^(BM)\.([0-9]{4})\.([0-9]{3})\.([0-9]{3})/[0-9]{2}$'},
        { 'format': 'BM.aaaa.nnn.mmm',          'regex': r'^(BM)\.([0-9]{4})\.([0-9]{3})\.([0-9]{3})$'},
        { 'format': 'BM.aaaa.nnn.mmm/',         'regex': r'^(BM)\.([0-9]{4})\.([0-9]{3})\.([0-9]{3})/$'},
        { 'format': 'BM.aaaa.nnn.mmm/ppp',      'regex': r'^(BM)\.([0-9]{4})\.([0-9]{3})\.([0-9]{3})/[0-9]{3}$'},
        { 'format': 'BM.aaaa.nnn.mm/pp',        'regex': r'^(BM)\.([0-9]{4})\.([0-9]{3})\.([0-9]{2})/[0-9]{2}$'},
        { 'format': 'BM.aaaa.nnn',              'regex': r'^(BM)\.([0-9]{4})\.([0-9]{3})$'},
        { 'format': 'BM.aaa.nnn.mmm/pp',        'regex': r'^(BM)\.([0-9]{3})\.([0-9]{3})\.([0-9]{3})/[0-9]{2}$'},
        { 'format': 'BM.aaa.nnn FANTOME',       'regex': r'^(BM)\.([0-9]{3})\.([0-9]{3}) FANTOME$'},
        { 'format': 'BM.aaa.nnn',               'regex': r'^(BM)\.([0-9]{3})\.([0-9]{3})$'},
        { 'format': 'BM.aaa.nnnBISoo/pp',       'regex': r'^(BM)\.([0-9]{3})\.([0-9]{3})BIS([0-9]{2})/[0-9]{2}$'},
        { 'format': 'BM.aaa.nnn.mmm.ppp',       'regex': r'^(BM)\.([0-9]{3})\.([0-9]{3})\.([0-9]{3})\.[0-9]{3}$'},
        { 'format': 'BM.aaa.nnn.mmm/ppp',       'regex': r'^(BM)\.([0-9]{3})\.([0-9]{3})\.([0-9]{3})/[0-9]{3}$'},
        { 'format': 'BM.aaa.nnn/pp',            'regex': r'^(BM)\.([0-9]{3})\.([0-9]{3})/[0-9]{2}$'},
        { 'format': 'BM.aaa.nnn-BIS.ooo/pp',    'regex': r'^(BM)\.([0-9]{3})\.([0-9]{3})-BIS\.([0-9]{3})/[0-9]{2}$'},
        { 'format': 'BM.aaaa.nnn.mmm/NN',       'regex': r'^(BM)\.([0-9]{4})\.([0-9]{3})\.([0-9]{3})/NN$'},
        { 'format': 'BM.aaa.nnn.mmm/pp-DEPOT',  'regex': r'^(BM)\.([0-9]{3})\.([0-9]{3})\.([0-9]{3})/[0-9]{2}-DEPOT$'},
        { 'format': 'BM.aaa.nnn.mmm-o>p',       'regex': r'^(BM)\.([0-9]{3})\.([0-9]{3})\.([0-9]{3})-[0-9]>[0-9]$'},
        { 'format': 'CY.aaaa.nnn',              'regex': r'^(CY)\.([0-9]{4})\.([0-9]{3})$'},
        { 'format': 'DI.aaaa.nnn.mmm',          'regex': r'^(DI)\.([0-9]{4})\.([0-9]{3})\.([0-9]{3})$'},
        { 'format': 'DI.aaaa.nnn.mmm/pp',       'regex': r'^(DI)\.([0-9]{4})\.([0-9]{3})\.([0-9]{3})/[0-9]{2}$'},
        { 'format': 'DI.aaa.nnn.mmm',           'regex': r'^(DI)\.([0-9]{3})\.([0-9]{3})\.([0-9]{3})$'},
        { 'format': 'DI.aaa.nnn.mmm/pp',        'regex': r'^(DI)\.([0-9]{3})\.([0-9]{3})\.([0-9]{3})/[0-9]{2}$'},
        { 'format': 'DI.aaa.nnn.mmm-o/p',       'regex': r'^(DI)\.([0-9]{3})\.([0-9]{3})\.([0-9]{3})-[0-9]/[0-9]$'},
        { 'format': 'FANTOME 2*',               'regex': r'FANTOME 2\*$'},

        ## yomguy
        { 'format': 'BM.aaaa.nnn.mm',       'regex': r'^(BM)\.([0-9]{4})\.([0-9]{3})\.([0-9]{3})$'},
        #{ 'format': 'BM.aaaa.nnn.mmm/pp:ii-jj', 'regex': r'^(BM)\.([0-9]{4})\.([0-9]{3})\.([0-9]{3})/([0-9]{2})\:([0-9]{2})\-([0-9]{2})$'},
        #{ 'format': 'BM.aaaa.nnn.mmm/ppp:ii-jj', 'regex': r'^(BM)\.([0-9]{4})\.([0-9]{3})\.([0-9]{3})/([0-9]{2})\:([0-9]{2})\-([0-9]{2})$'},
        #{ 'format': 'BM.aaaa.nnn.mmm:ii-jj',    'regex': r'^(BM)\.([0-9]{4})\.([0-9]{3})\.([0-9]{3}):([0-9]{2})\-([0-9]{2})$'},
        ]

ITEM_NEW_PATTERN = [
        { 'format': 'CNRSMH_I_aaaa_nnn_mmm',           'regex': r'^(CNRSMH)_I_([0-9]{4})_([0-9]{3})_([0-9]{3})$'},
        { 'format': 'CNRSMH_I_aaaa_nnn_mmm_tt',        'regex': r'^(CNRSMH)_I_([0-9]{4})_([0-9]{3})_([0-9]{3})_([0-9]{2})$'},
        { 'format': 'CNRSMH_I_aaaa_nnn_mmm_tt_pp',     'regex': r'^(CNRSMH)_I_([0-9]{4})_([0-9]{3})_([0-9]{3})_([0-9]{2})_([0-9]{2})$'},
        { 'format': 'CNRSMH_E_aaaa_nnn_mmm_tt',        'regex': r'^(CNRSMH)_E_([0-9]{4})_([0-9]{3})_([0-9]{3})_([0-9]{2})$'},
        { 'format': 'CNRSMH_E_aaaa_nnn_mmm_tt_pp',     'regex': r'^(CNRSMH)_E_([0-9]{4})_([0-9]{3})_([0-9]{3})_([0-9]{2,3})_([0-9]{2})$'},

        # yomguy
        { 'format': 'CNRSMH_I_aaaa_nnn_mm',           'regex': r'^(CNRSMH)_I_([0-9]{4})_([0-9]{3})_([0-9]{2})$'},
        ]

COLLECTION_PATTERN = [
        { 'format': 'CNRSMH_I_aaaa_nnn',           'regex': r'^(CNRSMH)_I_([0-9]{4})_([0-9]{3})$'},
        { 'format': 'CNRSMH_E_aaaa_nnn_mmm',        'regex': r'^(CNRSMH)_E_([0-9]{4})_([0-9]{3})_([0-9]{3})$'},
        ]


def check_name(patterns, name):
    match = False
    for pattern in patterns:
        match = re.match(pattern['regex'], name)
        if match:
            break
    return match


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


class CremCollection:

    def __init__(self, dir, logger):
        self.dir = dir
        self.dir_name = self.dir.split(os.sep)[-1]
        self.file_list = os.listdir(self.dir)
        self.logger = logger

    def xls_list(self):
        file_list = []
        for file in self.file_list:
            filename = os.path.basename(file)
            ext = os.path.splitext(file)[1]
            if not '.' == filename[0] and (ext == '.xls' or ext == '.XLS'):
                file_list.append(file)
        print file_list
        return file_list

    def wav_list(self):
        list = []
        for file in self.file_list:
            filename = os.path.basename(file)
            ext = os.path.splitext(file)[1]
            if not '.' == filename[0] and (ext == '.wav' or ext == '.WAV'):
                list.append(file)
            elif '.' == filename[0]:
                self.logger.write_error(file, 'Warning : fichier caché présent !')
        return list


class CremCSV:

    def __init__(self, file):
        self.csv_file = open(file, 'w')
        self.csv = csv.writer(self.csv_file,  delimiter=';')

    def close(self):
        self.csv_file.close()

class CremXLS:

    def __init__(self, file):
        self.first_row = 8
        self.original_col = 0
        self.new_col = 1
        self.book = xlrd.open_workbook(file)
        self.sheet = self.book.sheet_by_index(0)
        self.original_refs = self.original_refs()
        self.new_refs = self.new_refs()
        #print len(self.new_refs)
        while True:
            if len(self.original_refs) == 0 or len(self.new_refs) == 0:
                break
            else:
                if not 'CNRS' in self.new_refs[0].encode('utf8') \
                 and not  self.original_refs[0].encode('utf8') == '':
                    self.original_refs = self.original_refs[1:]
                    self.new_refs = self.new_refs[1:]
                else:
                    break

        self.size = max(len(self.new_refs), len(self.original_refs))

    def original_refs(self):
        col = self.sheet.col(self.original_col)
        list = []
        for cell in col[self.first_row:]:
            if cell.ctype == 1:
                list.append(cell.value)
        return list

    def new_refs(self):
        col = self.sheet.col(self.new_col)
        list = []
        for cell in col[self.first_row:]:
            if cell.ctype == 1:
                list.append(cell.value)
        return list


class CremItemFile:

    def __init__(self):
        self.media = ''

    def set_media(self, media):
        self.media = media

    def properties(self):
        self.frames = self.audio_file.get_nframes()
        self.samplerate = self.audio_file.get_samplerate()
        self.channels = self.audio_file.get_channels()
        self.format = self.audio_file.get_file_format()
        self.encoding = self.audio_file.get_encoding()


class CremCheck:

    def __init__(self, root_dir, log_file):
        self.root_dir = root_dir
        self.logger = Logger(log_file)
        dir_list = os.listdir(self.root_dir)
        list = []
        for dir in dir_list:
           if not dir[0] == '.':
               list.append(dir)
        self.dir_list = list

    def check_new_refs(self):
        for name in self.new_refs:
            return check_name(ITEM_PATTERN, name)

    def check(self):
        for dir in self.dir_list:
            collection = CremCollection(self.root_dir + dir, self.logger)
            msg = '************************ ' + collection.dir_name + ' ******************************'
            self.logger.write_info(collection.dir, msg[:70])

            xls_list = collection.xls_list()
            wav_list = collection.wav_list()

            if not check_name(COLLECTION_PATTERN, dir):
                self.logger.write_error(collection.dir, 'Le dossier de la collection est mal nommé -> SORTIE')
            elif len(xls_list) == 0:
                self.logger.write_error(collection.dir, 'PAS de fichier XLS dans le dossier collection -> SORTIE')
            elif len(xls_list) > 1:
                self.logger.write_error(collection.dir, 'Plusieurs fichiers XLS dans le dossier collection -> SORTIE')

            else:
                xls = CremXLS(self.root_dir + os.sep + dir + os.sep + xls_list[0])
                self.logger.write_info(collection.dir, 'XLS : ' + xls_list[0] + ' - Feuille : ' + xls.sheet.name.encode('utf8'))
                self.logger.write_info(collection.dir, 'Nombre d\'items détectés : ' + str(xls.size))
                csv_file = CremCSV(self.root_dir + dir + os.sep + collection.dir_name + '.csv')

                if len(wav_list) != xls.size:
                    self.logger.write_error(collection.dir, \
                    'Le nombre de références du fichier XLS (' + str(xls.size) + ') diffère du nombre de fichiers (' + str(len(wav_list)) + ')')

                temp_list = []
                item_file = CremItemFile()

                for i in range(0,xls.size):
                    error = False

                    try:
                        item_old = xls.original_refs[i]
                        #self.logger.write_error(collection.dir, item_old)
                    except:
                        item_old = ''
                        msg = 'Ligne ' + str(i+xls.first_row+1) + ' : l\'ancienne référence d\'item est inexistante'
                        self.logger.write_error(collection.dir, msg)
                        error = True
                        continue

                    try:
                        item = xls.new_refs[i]
                        #self.logger.write_error(collection.dir, item)
                    except:
                        item = ''
                        msg = 'Ligne ' + str(i+xls.first_row+1) + ' : la nouvelle référence d\'item est inexistante'
                        self.logger.write_error(collection.dir, msg)
                        error = True
                        continue

                    if not item in temp_list:
                        temp_list.append(item)
                    else:
                        msg =  'Ligne ' + str(i+xls.first_row+1) + ' : la référence d\'item ' + item.encode('utf8') + ' est multiple'
                        self.logger.write_error(collection.dir, msg)
                        error = True

                    #if not check_name(ITEM_OLD_PATTERN, item_old):
                        #msg = 'Ligne ' + str(i+xls.first_row+1) + ' : l\'ancienne référence d\'item ' + item_old.encode('utf8') + ' est mal formatée'
                        #self.logger.write_error(collection.dir, msg)

                    if not check_name(ITEM_NEW_PATTERN, item):
                        msg = 'Ligne ' + str(i+xls.first_row+1) + ' : la nouvelle référence d\'item ' + item.encode('utf8') + ' est mal formatée'
                        self.logger.write_error(collection.dir, msg)
                        error = True

                    if not collection.dir_name in item:
                        msg = 'Ligne ' + str(i+xls.first_row+1) + ' : la référence d\'item ' + item.encode('utf8') + ' ne correspond pas à celle de la collection'
                        self.logger.write_error(collection.dir, msg)
                        error = True

                    name_wav = item.encode('utf8') + '.wav'
                    if not name_wav in wav_list:
                        self.logger.write_error(collection.dir, 'Le fichier ' + item.encode('utf8') + '.wav n\'existe pas')
                    else:
                        item_file.set_media(collection.dir + os.sep + name_wav)
                        #if not item_file.is_wav():
                        #    self.logger.write_error(collection.dir, 'Le fichier ' + item.encode('utf8') + '.wav n\'est pas valide')
                        #    error = True

                    if not error:
                        csv_file.csv.writerow([xls.original_refs[i], xls.new_refs[i]])

                csv_file.close()

                for filename in wav_list:
                    if not check_name(ITEM_NEW_PATTERN, os.path.splitext(filename)[0]):
                        self.logger.write_error(collection.dir, 'Le nom du fichier ' + str(os.path.splitext(filename)[0]) + ' est mal formaté')

            msg = '********************************************************************************'
            self.logger.write_info(collection.dir, msg[:70])


def main():
    log_file = sys.argv[-1]
    root_dir = sys.argv[-2]
    log_tmp = log_file+'.tmp'

    c = CremCheck(root_dir, log_tmp)
    c.check()

    date = datetime.datetime.now().strftime("%x-%X").replace('/','_')
    shutil.copy(log_tmp,log_file+'-'+date+'.log')
    shutil.move(log_tmp,log_file)

if __name__ == '__main__':
    main()


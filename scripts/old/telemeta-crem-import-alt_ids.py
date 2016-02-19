#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2011 Guillaume Pellerin
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
import xlrd
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


class TelemetaAltIdsImport:

    def __init__(self, xls_file, log_file):
        self.logger = Logger(log_file)
        self.xls = xls_file
        self.row = 0

    def alt_ids_import(self):
        from telemeta.models import MediaCollection
        self.book = xlrd.open_workbook(self.xls)
        self.sheet = self.book.sheet_by_index(0)
        self.length = len(self.sheet.col(0))-1
        
        while True:
            ids = []
            self.row += 1
            row = self.sheet.row(self.row)
            if self.row == self.length:
                break
            collection_id = row[0].value
            cell_alt_id = row[1]
            if cell_alt_id.ctype == 1:
                for i in range(1,len(row)):
                    cell_alt_id = row[i]
                    if cell_alt_id.ctype == 1:
                        ids.append(cell_alt_id.value)
                alt_ids = ' '.join(ids)
                try:
                    collection = MediaCollection.objects.get(old_code=collection_id)
                    collection.alt_ids = alt_ids
                    collection.save()
                    print self.row, collection_id, alt_ids
                except:
                    msg = 'No collection found for this id'
                    self.logger.write_error(collection_id, msg)
                    continue
            
                
def print_usage(tool_name):
    print "Usage: "+tool_name+" <project_dir> <xls_file> <log_file>"
    print "  project_dir: the directory of the Django project which hosts Telemeta"
    print "  xls_file: the excel file containing all collection alt_ids"

def run():
    if len(sys.argv) < 3:
        print_usage(os.path.basename(sys.argv[0]))
        sys.exit(1)
    else:
        project_dir = sys.argv[-3]
        xls_file = sys.argv[-2]
        log_file = sys.argv[-1]
        sys.path.append(project_dir)
        import settings
        setup_environ(settings)
        t = TelemetaAltIdsImport(xls_file, log_file)
        t.alt_ids_import()

if __name__ == '__main__':
    run()

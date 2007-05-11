# -*- coding: utf-8 -*-
#
# Copyright (C) 2007 Parisson SARL
# Copyright (c) 2006-2007 Guillaume Pellerin <pellerin@parisson.com>
# All rights reserved.
#
# This software is licensed as described in the file COPYING, which
# you should have received as part of this distribution. The terms
# are also available at http://svn.parisson.org/telemeta/TelemetaLicense.
#
# Author: Guillaume Pellerin <pellerin@parisson.com>

import os
import string

from telemeta.export.core import *
from telemeta.export.api import IExporter
from mutagen.flac import FLAC

class FlacExporter(ExporterCore):
    """Defines methods to export to OGG Vorbis"""

    implements(IExporter)
    
    def __init__(self):
        self.item_id = ''
        self.source = ''
        self.metadata = {}
        self.options = {}
        self.description = ''
        self.dest = ''
        self.quality_default = '5'
        self.info = []
        
    def get_format(self):
        return 'FLAC'
    
    def get_file_extension(self):
        return 'flac'

    def get_mime_type(self):
        return 'application/flac'

    def get_description(self):
        return 'FIXME'

    def get_file_info(self):
        try:
            file1, file2 = os.popen4('metaflac --list "'+self.dest+'"')
            info = []
            for line in file2.readlines():
                info.append(clean_word(line[:-1]))
            self.info = info
            return self.info
        except IOError:
            return 'Exporter error [1]: file does not exist.'

    def set_cache_dir(self,path):
        """Set the directory where cached files should be stored. Does nothing
        if the exporter doesn't support caching. 
       
        The driver shouldn't assume that this method will always get called. A
        temporary directory should be used if that's not the case.
        """
        self.cache_dir = path

    def decode(self):
        try:
            file_name, ext = get_file_name(self.source)
            dest = self.cache_dir+os.sep+file_name+'.wav'
            os.system('flac -d -o "'+dest+'" "'+self.source+'"')
            self.source = dest
            return dest
        except IOError:
            return 'ExporterError [2]: decoder not compatible.'

    def write_tags(self):
        media = FLAC(self.dest)
        for tag in self.metadata.keys():
            if tag == 'COMMENT':
                media['DESCRIPTION'] = str(self.metadata[tag])
            else:
                media[tag] = str(self.metadata[tag])
        media.save()
        
    def process(self, item_id, source, metadata, options=None):
        self.item_id = item_id
        self.source = source
        self.metadata = metadata
        self.options = {}
        args = ''
        
        if not options is None:
            self.options = options
            
            if 'verbose' in self.options and self.options['verbose'] != '0':
                args = args
            else:
                args = args + ' -s '
                
            if 'flac_quality' in self.options:
                args = args+' -f -V -'+self.options['flac_quality']
            else:
                args = args+' -f -V -'+self.quality_default
        else:
            args = args+' -s -f -V -'+self.quality_default
    
        try:
            # Pre-proccessing (core)
            self.ext = self.get_file_extension()
            self.dest = self.pre_process(self.item_id,
                                         self.source,
                                         self.metadata,
                                         self.ext,
                                         self.cache_dir,
                                         self.options)

            # Encoding
            os.system('flac '+args+' -o "'+self.dest+'" "'+ \
                      self.source+'" > /dev/null')

            # Post-proccessing (self)
            self.write_tags()
            self.post_process(self.item_id,
                         self.source,
                         self.metadata,
                         self.ext,
                         self.cache_dir,
                         self.options)

            # Output
            return self.dest

        except IOError:
            return 'ExporterError [3]: source file does not exist.'


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
import subprocess

from telemeta.export.core import *
from telemeta.export.api import IExporter
#from mutagen.id3 import *


class Mp3Exporter(ExporterCore):
    """Defines methods to export to MP3"""

    implements(IExporter)
    
    def __init__(self):
        self.item_id = ''
        self.metadata = {}
        self.description = ''
        self.info = []
        self.source = ''
        self.dest = ''
        self.options = {}
        self.bitrate_default = '192'
        self.buffer_size = 0xFFFF
        self.dub2id3_dict = {'title': 'TIT2', #title2
                             'creator': 'TCOM', #composer
                     'creator': 'TPE1', #lead
                     'identifier': 'UFID', #Unique ID...
                     'identifier': 'TALB', #album
                     #'date': 'TYER', #year
                     'type': 'TCON', #genre
                     'publisher': 'TPUB', #comment
                     }

    def get_format(self):
        return 'MP3'
    
    def get_file_extension(self):
        return 'mp3'

    def get_mime_type(self):
        return 'audio/mpeg'

    def get_description(self):
        return "FIXME"

    def get_file_info(self):
        try:
            file_out1, file_out2 = os.popen4('mp3info "'+self.dest+'"')
            info = []
            for line in file_out2.readlines():
                info.append(clean_word(line[:-1]))
            self.info = info
            return self.info
        except IOError:
            return 'Exporter error [1]: file does not exist.'

    def decode(self):
        try:
            os.system('sox "'+self.source+'" -w -r 44100 -t wav "' \
                        +self.cache_dir+os.sep+self.item_id+'"')
            return self.cache_dir+os.sep+self.item_id+'.wav'
        except IOError:
            return 'ExporterError [2]: decoder not compatible.'

    def write_tags(self):
        """Write all ID3v2.4 tags by mapping dub2id3_dict dictionnary with the
            respect of mutagen classes and methods"""
        from mutagen import id3
        
        id3 = id3.ID3(self.dest)
        for tag in self.metadata.keys():
            if tag in self.dub2id3_dict.keys():
                frame_text = self.dub2id3_dict[tag]
                value = self.metadata[tag]
                #print frame_text+': '+value
                frame = mutagen.id3.Frames[frame_text](3,value)
                id3.add(frame)
        id3.save()

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
                args= args + '-S '  
            
            if 'mp3_bitrate' in self.options:
                args = args+'-b '+self.options['mp3_bitrate']
            else:
                args = args+'-b '+self.bitrate_default    
            #Copyrights, etc..
            args = args + ' -c -o '
        else:
            args = args + ' -S -c -o '
        
        if os.path.exists(self.source) and not iswav16(self.source):
            self.source = self.decode()
            
        try:
            # Pre-proccessing (core)
            self.ext = self.get_file_extension()
            self.dest = self.pre_process(self.item_id,
                            self.source,
                            self.metadata,
                            self.ext,
                            self.cache_dir,
                            self.options)
            
            # Initializing
            chunk = 0
            file_out = open(self.dest,'w')
            
            proc = subprocess.Popen( \
                    #'sox "'+self.source+'" -w -r 44100 -t wav -c2 - '+ 
                    #'| lame '+args+' --tc "default" -',
                    'lame '+args+' --tc "default" "'+self.source+'" -',
                    shell=True,
                    bufsize=self.buffer_size,
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    close_fds=True)
                
            chunk = proc.stdout.read(self.buffer_size)
            yield chunk
            file_out.write(chunk)
           
            # Processing
            while chunk:
                chunk = proc.stdout.read(self.buffer_size)
                yield chunk
                file_out.write(chunk)           
           
            file_out.close()
            
            # Encoding
            # os.system('lame '+args+' --tc "default" "'+self.source+
            #                        '" "'+self.dest+'"')
            
            # Post-proccessing (self)
            self.write_tags()
            self.post_process(self.item_id,
                         self.source,
                         self.metadata,
                         self.ext,
                         self.cache_dir,
                         self.options)
                        
            # Output
            # return self.dest

        except IOError:
            yield 'ExporterError [3]: source file does not exist.'


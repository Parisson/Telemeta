# -*- coding: utf-8 -*-
#
# Copyright (c) 2007-2009 Guillaume Pellerin <yomguy@parisson.com>

# This software is a computer program whose purpose is to backup, analyse,
# transcode and stream any audio content with its metadata over a web frontend.

# This software is governed by the CeCILL  license under French law and
# abiding by the rules of distribution of free software.  You can  use,
# modify and/ or redistribute the software under the terms of the CeCILL
# license as circulated by CEA, CNRS and INRIA at the following URL
# "http://www.cecill.info".

# As a counterpart to the access to the source code and  rights to copy,
# modify and redistribute granted by the license, users are provided only
# with a limited warranty  and the software's author,  the holder of the
# economic rights,  and the successive licensors  have only  limited
# liability.

# In this respect, the user's attention is drawn to the risks associated
# with loading,  using,  modifying and/or developing or reproducing the
# software by the user in light of its specific status of free software,
# that may mean  that it is complicated to manipulate,  and  that  also
# therefore means  that it is reserved for developers  and  experienced
# professionals having in-depth computer knowledge. Users are therefore
# encouraged to load and test the software's suitability as regards their
# requirements in conditions enabling the security of their systems and/or
# data to be ensured and,  more generally, to use and operate it in the
# same conditions as regards security.

# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL license and that you accept its terms.

# Author: Guillaume Pellerin <pellerin@parisson.com>

import os
import string
import subprocess

from telemeta.export.core import *
from telemeta.export.api import IExporter
from mutagen.flac import FLAC
from tempfile import NamedTemporaryFile

class FlacExporter(ExporterCore):
    """Defines methods to export to FLAC"""

    implements(IExporter)
    
    def __init__(self):
        self.item_id = ''
        self.source = ''
        self.metadata = {}
        self.options = {}
        self.description = ''
        self.dest = ''
        self.quality_default = '-5'
        self.info = []
        self.buffer_size = 0xFFFF

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
        except:
            raise IOError('ExporterError: metaflac is not installed or ' + \
                           'file does not exist.')

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
        except:
            raise IOError('ExporterError: decoder is not compatible.')

    def write_tags(self, file):
        media = FLAC(file)
        for tag in self.metadata.keys():
            if tag == 'COMMENT':
                media['DESCRIPTION'] = str(self.metadata[tag])
            else:
                media[tag] = str(self.metadata[tag])
        try:
            media.save()
        except:
            raise IOError('ExporterError: cannot write tags.')

    def get_args(self,options=None):
        """Get process options and return arguments for the encoder"""
        args = []
        if not options is None:
            self.options = options
            if not ('verbose' in self.options and self.options['verbose'] != '0'):
                args.append('-s')
            if 'flac_quality' in self.options:
                args.append('-f ' + self.options['flac_quality'])
            else:
                args.append('-f ' + self.quality_default)
        else:
            args.append('-s -f ' + self.quality_default)

        #for tag in self.metadata.keys():
            #value = clean_word(self.metadata[tag])
            #args.append('-c %s="%s"' % (tag, value))
            #if tag in self.dub2args_dict.keys():
                #arg = self.dub2args_dict[tag]
                #args.append('-c %s="%s"' % (arg, value))

        return args

    def process(self, item_id, source, metadata, options=None):
        self.item_id = item_id
        self.source = source
        self.metadata = metadata
        self.args = self.get_args(options)
        self.ext = self.get_file_extension()
        self.args = ' '.join(self.args)
        self.command = 'sox "%s" -s -q -b 16 -r 44100 -t wav -c2 - | flac -c %s - ' % (self.source, self.args)

        # Pre-proccessing
        self.dest = self.pre_process(self.item_id,
                                         self.source,
                                         self.metadata,
                                         self.ext,
                                         self.cache_dir,
                                         self.options)

        # Processing (streaming + cache writing)
        stream = self.core_process(self.command, self.buffer_size, self.dest)

        for chunk in stream:
            pass

        self.write_tags(self.dest)
        file = open(self.dest,'r')
        
        while True:
            chunk = file.read(self.buffer_size)
            if len(chunk) == 0:
                break
            yield chunk

        file.close()

        # Post-proccessing
        #self.post_process(self.item_id,
                         #self.source,
                         #self.metadata,
                         #self.ext,
                         #self.cache_dir,
                         #self.options)


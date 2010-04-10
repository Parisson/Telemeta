# -*- coding: utf-8 -*-
#
# Copyright (C) 2007 Parisson SARL
# Copyright (c) 2006-2007 Guillaume Pellerin <pellerin@parisson.com>

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
                             'type': 'TCON', #genre
                             'publisher': 'TPUB', #comment
                             #'date': 'TYER', #year
                             }
        self.dub2args_dict = {'title': 'tt', #title2
                             'creator': 'ta', #composerS
                             'relation': 'tl', #album
                             #'type': 'tg', #genre
                             'publisher': 'tc', #comment
                             'date': 'ty', #year
                             }
    def get_format(self):
        return 'MP3'

    def get_file_extension(self):
        return 'mp3'

    def get_mime_type(self):
        return 'audio/mpeg'

    def get_description(self):
        return "FIXME"

    def set_cache_dir(self,path):
       self.cache_dir = path

    def get_file_info(self):
        try:
            file_out1, file_out2 = os.popen4('mp3info "'+self.dest+'"')
            info = []
            for line in file_out2.readlines():
                info.append(clean_word(line[:-1]))
            self.info = info
            return self.info
        except:
            raise IOError('ExporterError: file does not exist.')

    def decode(self):
        try:
            os.system('sox "'+self.source+'" -s -q -r 44100 -t wav "' \
                        +self.cache_dir+os.sep+self.item_id+'"')
            return self.cache_dir+os.sep+self.item_id+'.wav'
        except:
            raise IOError('ExporterError: decoder is not compatible.')

    def write_tags(self):
        """Write all ID3v2.4 tags by mapping dub2id3_dict dictionnary with the
            respect of mutagen classes and methods"""
        from mutagen import id3
        id3 = id3.ID3(self.dest)
        for tag in self.metadata.keys():
            if tag in self.dub2id3_dict.keys():
                frame_text = self.dub2id3_dict[tag]
                value = self.metadata[tag]
                frame = mutagen.id3.Frames[frame_text](3,value)
                try:
                    id3.add(frame)
                except:
                    raise IOError('ExporterError: cannot tag "'+tag+'"')
        try:
            id3.save()
        except:
            raise IOError('ExporterError: cannot write tags')

    def get_args(self, options=None):
        """Get process options and return arguments for the encoder"""
        args = []
        if not options is None:
            self.options = options
            if not ( 'verbose' in self.options and self.options['verbose'] != '0' ):
                args.append('-S')
            if 'mp3_bitrate' in self.options:
                args.append('-b ' + self.options['mp3_bitrate'])
            else:
                args.append('-b '+self.bitrate_default)
            #Copyrights, etc..
            args.append('-c -o')
        else:
            args.append('-S -c -o')

        for tag in self.metadata:
            name = tag[0]
            value = clean_word(tag[1])
            if name in self.dub2args_dict.keys():
                arg = self.dub2args_dict[name]
                args.append('--' + arg + ' "' + value + '"')
        return args

    def process(self, item_id, source, metadata, options=None):
        self.item_id = item_id
        self.source = source
        self.metadata = metadata
        self.args = self.get_args(options)
        self.ext = self.get_file_extension()
        self.args = ' '.join(self.args)
        self.command = 'sox "%s" --single-threaded -q -b 16 -t wav - | lame %s -' % (self.source, self.args)
        #self.command = 'lame %s "%s" -' % (self.args, self.source)

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
            yield chunk

        # Post-proccessing
        #self.post_process(self.item_id,
                         #self.source,
                         #self.metadata,
                         #self.ext,
                         #self.cache_dir,
                         #self.options)


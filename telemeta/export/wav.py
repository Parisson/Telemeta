# -*- coding: utf-8 -*-
#
# Copyright Guillaume Pellerin, (2006-2009)
# <yomguy@parisson.com>

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

from telemeta.export.core import *
from telemeta.export.api import IExporter

class WavExporter(ExporterCore):
    """Defines methods to export to WAV"""

    implements(IExporter)
    
    def __init__(self):
        self.item_id = ''
        self.metadata = {}
        self.description = ''
        self.info = []
        self.source = ''
        self.dest = ''
        self.options = {}
        self.buffer_size = 0xFFFF

    def get_format(self):
        return 'WAV'
    
    def get_file_extension(self):
        return 'wav'

    def get_mime_type(self):
        return 'audio/x-wav'

    def get_description(self):
        return 'FIXME'

    def get_file_info(self):
        try:
            file1, file2 = os.popen4('wavinfo "'+self.dest+'"')
            info = []
            for line in file2.readlines():
                info.append(clean_word(line[:-1]))
            self.info = info
            return self.info
        except:
            raise IOError('ExporterError: wavinfo id not installed or file does not exist.')

    def set_cache_dir(self,path):
        self.cache_dir = path

    def decode(self):
        try:
            file_name, ext = get_file_name(self.source)
            dest = self.cache_dir+os.sep+file_name+'.wav'
            os.system('sox "'+self.source+'" -s -r 44100 -t wav -c2 "'+ \
                      dest+'.wav"')
            self.source = dest
            return dest
        except:
            raise IOError('ExporterError: decoder is not compatible.')

    def write_tags(self):
        # Create metadata XML file !
        self.write_metadata_xml(self.dest+'.xml')
    
    def create_md5_key(self):
        """ Create the md5 keys of the dest """
        try:
            os.system('md5sum -b "'+self.dest+'" >"'+self.dest+'.md5"')
        except:
            raise IOError('ExporterError: cannot create the md5 key.')
    
    def create_par_key(self):
        """ Create the par2 keys of the dest """
        args = 'c -n1 '
        if 'verbose' in self.options and self.options['verbose'] != '0':
            args = args
        else:
            args = args + '-q -q '

        try:
            os.system('par2 '+args+' "'+self.dest+'"')
        except:
            raise IOError('ExporterError: cannot create the par2 key.')

    def process(self, item_id, source, metadata, options=None):
        self.item_id = item_id
        self.source = source
        self.metadata = metadata
        self.options = {}

        if not options is None:
            self.options = options

        # Pre-proccessing
        self.ext = self.get_file_extension()
        self.dest = self.pre_process(self.item_id,
                                        self.source,
                                        self.metadata,
                                        self.ext,
                                        self.cache_dir,
                                        self.options)

        # Initializing
        file_in = open(self.source,'rb')
        file_out = open(self.dest,'w')

        # Core Processing
        while True:
            chunk = file_in.read(self.buffer_size)
            if len(chunk) == 0:
                break
            yield chunk
            file_out.write(chunk)

        file_in.close()
        file_out.close()

        # Create the md5 key
        #if 'md5' in self.metadata and self.metadata['md5']:
        self.create_md5_key()

        # Create the par2 key
        #if 'par2' in self.metadata and self.metadata['par2']:
        #self.create_par_key()

        # Pre-proccessing
        self.post_process(self.item_id,
                        self.source,
                        self.metadata,
                        self.ext,
                        self.cache_dir,
                        self.options)



            #if self.compare_md5_key():
            #os.system('cp -a "'+self.source+'" "'+ self.dest+'"')
            #print 'COPIED'


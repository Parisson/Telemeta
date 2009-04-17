# -*- coding: utf-8 -*-
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
from telemeta.core import *
#from telemeta.visualization.api import IMediaItemVisualizer
from django.conf import settings
from tempfile import NamedTemporaryFile
import os
import random
import subprocess
import signal
import time

class OctaveCoreVisualizer(Component):
    """Parent class for Octave visualization drivers"""

    def get_mFile_line(self):
        octave_path = os.path.dirname(__file__) + '/octave/'
        mFile_path = os.path.dirname(__file__) + '/octave/' + self.mFile
        mFile = open(mFile_path,'r')
        
        for line in mFile.readlines():
            if '$OCTAVEPATH' in line:
                line = line.replace('$OCTAVEPATH','"'+octave_path+'"')
            if '$WAVFILE' in line:
                line = line.replace('$WAVFILE','"'+self.wavFile_path+'"')
            if '$IMGFILE' in line:
                line = line.replace('$IMGFILE','"'+self.ppmFile.name+'"')
            yield line
            
        mFile.close()

    def set_m_file(self,mFile):
        self.mFile = mFile

    def get_wav_path(self, media_item):
        self.wavFile_path = media_item.file.path
        
    def octave_to_png_stream(self, media_item):
        self.buffer_size = 0xFFFF
        self.trans_type = 'ppm'
        self.mat_type = 'm'
        self.ppmFile = NamedTemporaryFile(suffix='.'+self.trans_type)
        self.wavFile = self.get_wav_path(media_item)
        mFile_tmp = NamedTemporaryFile(suffix='.'+self.mat_type)
        mFile_name = mFile_tmp.name
        mFile_tmp.close()
        mFile_tmp = open(mFile_name,'w')
        self.pngFile = NamedTemporaryFile(suffix='.png')
        command = ['octave', mFile_name]

        for line in self.get_mFile_line():
            mFile_tmp.write(line)
        mFile_tmp.close()

        # Compute
        proc = subprocess.Popen(command, stdout = subprocess.PIPE)               
        proc.wait()
        
        # Convert
        os.system('convert ' + self.ppmFile.name + \
                  ' -scale x250 ' + self.pngFile.name)
        
        # Stream
        while True:
            buffer = self.pngFile.read(self.buffer_size)
            if len(buffer) == 0:
                break
            yield buffer

        self.ppmFile.close()
        self.pngFile.close()
        os.remove(mFile_name)
        
        


from telemeta.core import *
from telemeta.export import *
from telemeta.visualization.api import IMediaItemVisualizer
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
        self.wavFile_path = settings.MEDIA_ROOT + '/' + media_item.file
        
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
        print command
        print self.pngFile.name

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
        while True  :
            buffer = self.pngFile.read(self.buffer_size)
            if len(buffer) == 0:
                break
            yield buffer

        self.ppmFile.close()
        self.pngFile.close()
        #os.remove(mFile_name)
        
        

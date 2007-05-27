
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
        
        while True:
            line = mFile.readline()
            if 'quit' in line:
                break
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

        self.pngFile = NamedTemporaryFile(suffix='.png')
        self.ppmFile = NamedTemporaryFile(suffix='.'+self.dest_type)
        self.wavFile = self.get_wav_path(media_item)
        #command = 'octave2.9 ' + self.mFile_tmp.name
        command = 'octave2.9'
                
        proc = subprocess.Popen(command,
                                shell = True,
                                #bufsize = buffer_size,
                                stdin = subprocess.PIPE,
                                stdout = subprocess.PIPE,
                                close_fds = True)

        for line in self.get_mFile_line():
            proc.stdin.write(line)

        # Wait for ppm
        status = os.stat(self.ppmFile.name).st_size
        while True:
            if status == os.stat(self.ppmFile.name).st_size and status != 0:
                break
            status = os.stat(self.ppmFile.name).st_size
            #print status
        time.sleep(1)

        # Convert
        os.system('convert ' + self.ppmFile.name + ' -scale 300x300 ' + self.pngFile.name)

        os.kill(proc.pid, signal.SIGKILL)

        # Stream
        while True  :
            buffer = self.pngFile.read(self.buffer_size)
            if len(buffer) == 0:
                break
            yield buffer

        self.ppmFile.close()
        self.pngFile.close()

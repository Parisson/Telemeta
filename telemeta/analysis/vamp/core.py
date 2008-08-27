
from telemeta.core import *
from django.conf import settings
from tempfile import NamedTemporaryFile
from telemeta.analysis.api import IMediaItemAnalyzer
import os
import random
import subprocess
import signal
import time

class VampCoreAnalyzer:
    """Parent class for Vamp plugin drivers"""

    def __init__(self):
        self.vamp_path = '/usr/lib/vamp/'
        # needs vamp-examples package
        self.host = 'vamp-simple-host'
        self.buffer_size = 0xFFFF
               
    def get_id(self):
        return "vamp_plugins"

    def get_name(self):
        return "Vamp plugins"

    def get_unit(self):
        return ""

    def get_plugins_list(self):
        if os.path.exists(self.vamp_path):
            args = ' --list-outputs'
            command = self.host + args
            #tmp_file = NamedTemporaryFile()
            data = self.core_process(command, self.buffer_size)
            text = ''
            plugins = []
            for chunk in data:
                text = text + chunk
            lines = text.split('\n')
            for line in lines:
                if line != '':
                    struct = line.split(':')
                    struct = struct[1:]
                    plugins.append(struct)
            return plugins
        else:
            return []

    def get_wav_path(self, media_item):
        return settings.MEDIA_ROOT + '/' + media_item.file
        #return media_item
        
    def render(self, plugin, media_item):
        self.wavFile = self.get_wav_path(media_item)
        args = ' -s ' + ':'.join(plugin) + ' ' + str(self.wavFile)
        command = command = self.host + args
        data = self.core_process(command, self.buffer_size)
        string = ''
        values = {}
        for chunk in data:
            string = string + chunk
        lines = string.split('\n')
        for line in lines:
            if line != '':
                struct = line.split(':')
                values[struct[0]] = struct[1]
        return values

    def core_process(self, command, buffer_size):
        """Encode and stream audio data through a generator"""
        
        __chunk = 0

        try:
            proc = subprocess.Popen(command,
                    shell = True,
                    bufsize = buffer_size,
                    stdin = subprocess.PIPE,
                    stdout = subprocess.PIPE,
                    close_fds = True)
        except:
            raise VampProcessError('Command failure:', command, proc)
            
        # Core processing
        while True:
            __chunk = proc.stdout.read(buffer_size)
            status = proc.poll()
            if status != None and status != 0:
                raise VampProcessError('Command failure:', command, proc)
            if len(__chunk) == 0:
                break
            yield __chunk
        

class VampProcessError(TelemetaError):

    def __init__(self, message, command, subprocess):
        self.message = message
        self.command = str(command)
        self.subprocess = subprocess

    def __str__(self):
        if self.subprocess.stderr != None:
            error = self.subprocess.stderr.read()
        else:
            error = ''
        return "%s ; command: %s; error: %s" % (self.message,
                                                self.command,
                                                error)

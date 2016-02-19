#!/usr/bin/python

import os, sys, string
import logging

class Logger:
    """A logging object"""

    def __init__(self, file):
        self.logger = logging.getLogger('myapp')
        self.hdlr = logging.FileHandler(file)
        self.formatter = logging.Formatter('%(message)s')
        self.hdlr.setFormatter(self.formatter)
        self.logger.addHandler(self.hdlr)
        self.logger.setLevel(logging.INFO)

log_file = 'thumbs.log'
logger = Logger(log_file)
root_dir = sys.argv[-1]
args = sys.argv[1:-1]
source_format = 'webm'
done = []
preview_tc = '00:00:05'

if os.path.exists(log_file):
    f = open(log_file, 'r')
    for line in f.readlines():
        done.append(line[:-1])
    f.close()

for root, dirs, files in os.walk(root_dir):
    for file in files:
        path = os.path.abspath(root + os.sep + file)
        name, ext = os.path.splitext(file)
        if ext[1:] == source_format:
            dest = os.path.abspath(root + os.sep + name + '.png')
            if not dest in done or '--force' in args:
                command = 'ffmpeg -ss '+ preview_tc + ' -i ' + path + '  -y ' + dest
                os.system(command)
                logger.logger.info(dest)

print "DONE!"

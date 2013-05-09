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

log_file = 'transcoding.log'
logger = Logger(log_file)
root_dir = sys.argv[-1]
args = sys.argv[1:-1]
source_format = 'webm'
done = []
ffmpeg_args = {'mp3' : ' -vn -acodec libmp3lame -aq 6 -ac 1 ',
               'ogg' : ' -vn -acodec copy ',
               'mp4' : ' -vcodec libx264 -r 24 -b 512k -threads 6 -acodec libfaac -ar 48000 -ab 96k -ac 1 ',
              }

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
            for format in ffmpeg_args.keys():
                dest = os.path.abspath(root + os.sep + name + '.' + format)
                if not dest in done or '--force' in args:
                    command = 'ffmpeg -i ' + path + ffmpeg_args[format] + ' -y ' + dest
                    os.system(command)
                    logger.logger.info(dest)

print "DONE!"

#!/usr/bin/python

import os, sys, string
import logging


class Logger:
    """A logging object"""

    def __init__(self, file):
        self.logger = logging.getLogger('myapp')
        self.hdlr = logging.FileHandler(file)
        self.formatter = logging.Formatter('%(asctime)s %(message)s')
        self.hdlr.setFormatter(self.formatter)
        self.logger.addHandler(self.hdlr)
        self.logger.setLevel(logging.INFO)


source_format = 'webm'
preview_tc = '00:00:05'

ffmpeg_args = {'mp3' : ' -i %i -vn -acodec libmp3lame -aq 6 -ac 1',
               'ogg' : ' -i %i -vn -acodec copy',
               'mp4' : ' -i %i -vcodec libx264 -r 24 -b 512k -threads 6 -acodec libfaac -ar 48000 -ab 96k -ac 1',
               'png' : ' -ss ' + preview_tc + '-i %i',
              }

logger = Logger(log_file)
args = sys.argv[1:]
log_file = args[-1]
root_dir = args[-2]

for root, dirs, files in os.walk(root_dir):
    for file in files:
        path = os.path.abspath(root + os.sep + file)
        name, ext = os.path.splitext(file)
        if ext[1:] == source_format:
            for format in ffmpeg_args.keys():
                local_file = name + '.' + format
                dest = os.path.abspath(root + os.sep + local_file)
                local_files = os.listdir(root)
                if not local_file in local_files or '--force' in args:
                    command = ffmpeg_args[format] % path + ' -y ' + dest
                    logger.logger.info(command)
                    if not '--dry-run' in args:
                        os.system(command)


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
threads = 4

ffmpeg_args = {
               'mp3' : '-i "%s" -vn -acodec libmp3lame -aq 6 -ac 2',
               'ogg' : '-i "%s" -vn -acodec copy',
               'mp4' : '-i "%s" -vcodec libx264 -threads ' + str(threads) + \
                       ' -c:v libx264 -crf 17 -maxrate 1100k -bufsize 1835k -acodec libfaac -ab 96k -ac 2',
               'png' : '-ss ' + preview_tc + ' -i "%s"',
              }

args = sys.argv[1:]
log_file = args[-1]
root_dir = args[-2]
logger = Logger(log_file)

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
                    command = 'ffmpeg -loglevel 0 ' + ffmpeg_args[format] % path + ' -y "' + dest + '"'
                    logger.logger.info(command)
                    if not '--dry-run' in args:
                        os.system(command)

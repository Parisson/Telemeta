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


class TelemetaTranscode(object):
    """docstring for TelemetaTranscode"""

    threads = 4
    source_formats = ['webm', 'mp4']
    dest_formats = {
                   'mp3' : '-vn -acodec libmp3lame -aq 6',
                   'ogg' : '-vn -acodec libvorbis -aq 6',
                   'mp4' : '-vcodec libx264 -threads ' + str(threads) + \
                           ' -c:v libx264 -crf 17 -maxrate 1100k -bufsize 1835k -acodec libfaac -ab 96k',
                   'png' : '',
                   'webm' : '-vcodec libvpx -threads ' + str(threads) + \
                           ' -c:v libvpx -crf 17 -b:v 1100k',
                  }


    def __init__(self, args):
        self.args = args
        self.log_file = args[-1]
        self.root_dir = args[-2]
        self.logger = Logger(self.log_file)


    def get_ext_in_dir(self, extension, root):
        files = os.listdir(root)
        exts = []
        for f in files:
            name, ext = os.path.splitext(f)
            ext = ext[1:]
            if not ext in exts:
                exts.append(ext)
        return extension in exts

    def run(self):
        for root, dirs, files in os.walk(self.root_dir):
            for file in files:
                path = os.path.abspath(root + os.sep + file)
                name, ext = os.path.splitext(file)
                ext = ext[1:]
                if ext in self.source_formats:
                    for format, ffmpeg_args in self.dest_formats.iteritems():
                        local_file = name + '.' + format
                        dest = os.path.abspath(root + os.sep + local_file)
                        local_files = os.listdir(root)
                        if not (local_file in local_files or self.get_ext_in_dir(format, root)) or '--force' in self.args:
                            if ext == 'webm' and format == 'ogg':
                                ffmpeg_args = '-vn -acodec copy'
                            command = 'ffmpeg -loglevel 0 -i "' + path + '" ' + ffmpeg_args + ' -y "' + dest + '"'
                            self.logger.logger.info(command)
                            if not '--dry-run' in self.args:
                                os.system(command)
                            else:
                                print command


if __name__ == '__main__':
    t = TelemetaTranscode(sys.argv[1:])
    t.run()

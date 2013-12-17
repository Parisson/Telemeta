#!/usr/bin/python

import os, sys, psutil
import datetime
from ebml.utils.ebml_data import *

class FixCheckMedia(object):

    def __init__(self, dir, tmp_dir):
        self.dir = dir
        self.tmp_dir = tmp_dir
        if not os.path.exists(self.tmp_dir):
            os.makedirs(self.tmp_dir)

    def process(self):
        webm_fixed_log = 'webm.fixed'
        webm_tofix_log = 'webm.tofix'
        mp3_fixed_log = 'mp3.fixed'
        mp3_tofix_log = 'mp3.tofix'

        for root, dirs, files in os.walk(self.dir):
            for filename in files:
                source = root + os.sep + filename
                name = os.path.splitext(filename)[0]
                ext = os.path.splitext(filename)[1][1:]

                if ext == 'webm' and os.path.getsize(source):
                    dir_files = os.listdir(root)

                    if not webm_fixed_log in dir_files:
                        print source    
                        self.fix_webm(source)
                        f = open(root + os.sep + webm_fixed_log, 'w')
                        f.close()
                        if os.path.exists(root + os.sep + webm_tofix_log):
                            os.remove(root + os.sep + webm_tofix_log)
            
                    if mp3_tofix_log in dir_files and not mp3_fixed_log in dir_files:
                        for file in dir_files:
                            dest_ext = os.path.splitext(file)[1][1:]
                            if dest_ext == 'mp3':
                                dest = root + os.sep + file
                                print dest
                                self.fix_mp3(source, dest)
                                f = open(root + os.sep + mp3_fixed_log, 'w')
                                f.close()
                                if os.path.exists(root + os.sep + mp3_tofix_log):
                                    os.remove(root + os.sep + mp3_tofix_log)
                                #break


    def hard_fix_webm(self, path):
        try:
            tmp_file = self.tmp_dir + 'out.webm '
            command = 'ffmpeg -loglevel 0 -i "'+ path + '" -vcodec libvpx -vb 500k -acodec libvorbis -aq 7 -f webm -y "' + tmp_file + '" > /dev/null'
            print command
            os.system(command)
            command = 'mv '  + tmp_file + path
            os.system(command)
        except:
            pass


    def fix_webm(self, path):
        try:
            tmp_file = self.tmp_dir + 'out.webm'
            command = '/usr/local/bin/ffmpeg -loglevel 0 -i "' + path + '" -vcodec copy -acodec copy -f webm -y "' + tmp_file + '" > /dev/null'
            print command
            os.system(command)
            ebml_obj = EBMLData(tmp_file)
            offset = ebml_obj.get_first_cluster_seconds()
            command = '/usr/local/bin/ffmpeg -loglevel 0 -ss ' + str(offset) + ' -i "' + tmp_file + '" -vcodec copy -acodec copy -f webm -y "' + path + '" > /dev/null'
            print command
            os.system(command)
        except:
            pass

    def fix_mp3(self, source, path):
        try:
            command = '/usr/local/bin/ffmpeg -loglevel 0 -i "'+ source + '" -vn -aq 6 -y "' + path + '" > /dev/null'
            print command
            os.system(command)
        except:
            pass

def get_pids(name, args=None):
    """Get a process pid filtered by arguments and uid"""
    pids = []
    for proc in psutil.process_iter():
        if proc.cmdline:
            if name == proc.name:
                if args:
                    if args in proc.cmdline:
                        pids.append(proc.pid)
                else:
                    pids.append(proc.pid)
    return pids

dir = sys.argv[-2]
tmp_dir = sys.argv[-1]

path =  os.path.abspath(__file__)
pids = get_pids('python2.6',args=path)

print datetime.datetime.now()
if len(pids) <= 1:
    print 'starting process...'
    f = FixCheckMedia(dir, tmp_dir)
    f.process()
    print 'process finished.\n'
else:
    print 'already started !\n'


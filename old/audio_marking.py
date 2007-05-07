#!/usr/bin/python
# *coding: utf-8*
#
# Copyright (c) 2006-2007 Guillaume Pellerin <pellerin@parisson.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Library General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301 USA

import os, sys, re, string
import tag_tools
from audio_tools import *

def make_auto_mark(dir_in,file_in):
    media_in = dir_in+file_in
    artist_no_ = string.replace(tag_tools.get_tag_value('ARTIST'),'_',' ')
    title_no_ = string.replace(tag_tools.get_tag_value('TITLE'),'_',' ')
    description_no_ = string.replace(tag_tools.get_tag_value('COMMENT'),'_',' ')
    os.system('echo "This is: '+title_no_+'. By '+artist_no_+'. It is '+description_no_+'" | text2wave -f 44100 -o "'+media_in+'_mark.tmp"')
    #os.system('normalize-audio "'+media_in+'_mark.tmp"')
    os.system('sox "'+media_in+'_mark.tmp" -t wav -c2 "'+media_in+'_mark.wav" vol 10.0 dB compand 50,20 -80,-80,-25,-35,-15,-27,-5,-19,0,-15 15')
    os.system('rm '+dir_in+'*.tmp')

def mark_audio(dir_in,file_in,audio_marking_file,audio_marking_timeline):
    media_in = dir_in+file_in
    file_length_sec = audio_length_sec(media_in)
    audio_mark_length_sec = audio_length_sec(audio_marking_file)
    ecasound_phrase = ''
    audio_gain = str(100+100*len(audio_marking_timeline))

    for timeline in audio_marking_timeline:
        audio_marking_ecasound_filename = file_in+'_'+timeline+'.ewf'
        audio_marking_ecasound_path = dir_in+file_in+'_'+timeline+'.ewf'
        audio_marking_ecasound_file=open(audio_marking_ecasound_path,'w')
        audio_marking_ecasound_file.write('-- '+audio_marking_ecasound_filename+' --\n')
        audio_marking_ecasound_file.write('source = '+audio_marking_file+'\n')
        if timeline == 'b':
            mark_offset = '0'
            ecasound_phrase = '-a:2 -i:"'+audio_marking_ecasound_path+'" -ea:'+audio_gain+' '
        if timeline == 'm':
            mark_offset = str(file_length_sec/2)
            ecasound_phrase = ecasound_phrase+'-a:3 -i:"'+audio_marking_ecasound_path+'" -ea:'+audio_gain+' '
        if timeline == 'e':
            mark_offset = str(file_length_sec-audio_mark_length_sec)
            ecasound_phrase = ecasound_phrase+'-a:4 -i:"'+audio_marking_ecasound_path+'" -ea:'+audio_gain+' '
        audio_marking_ecasound_file.write('offset = '+mark_offset+'.0\n')
        audio_marking_ecasound_file.write('start-position = 0.0\n')
        audio_marking_ecasound_file.write('length = '+str(audio_mark_length_sec)+'.0\n')
        audio_marking_ecasound_file.write('looping = false\n')
        audio_marking_ecasound_file.write('--cut--\n')
        audio_marking_ecasound_file.close()
    os.system('ecasound -a:1 -i:"'+media_in+'" -ea:'+audio_gain+' '+ecasound_phrase+' -a:all -o "'+dir_in+'marked_'+file_in+'"')


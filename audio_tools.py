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

def encode(enc_type,dir_in,file_in,dir_out,file_out):
	media_in = dir_in+file_in
	media_out = dir_out+file_out

	if enc_type == 'flac' :
		quality = tag_tools.get_opt_value(enc_type+'_quality')
		os.system('flac -f -V -q '+quality+' -o "'+media_out+'" "'+media_in+'"')

	if enc_type == 'ogg':
		bitrate = tag_tools.get_opt_value(enc_type+'_bitrate')
	 	os.system('oggenc -b '+bitrate+' -o "'+media_out+'" "'+media_in+'"')

	if enc_type == 'mp3':
		bitrate = tag_tools.get_opt_value(enc_type+'_bitrate')
		tag='temp'
		os.system('lame -b '+tag+' --ta "'+tag+'" --tt "'+tag+'" --tl "'+tag+'" --ty '+tag+' --tg "Other" --tc "'+tag+'" "'+media_in+'" "'+media_out+'"')

	if enc_type == 'wav':
		if iswav16(media_in):
			os.system('cp -a "'+media_in+'" "'+media_out+'"')
		else:
			os.system('sox "'+media_in+'" -w -r 44100 -t wav -c2 "'+media_out+'"')

#	if enc_type == 'ogg' and ismp3(media_in):
#                os.system('mp32ogg --verbose "'+file_in+'" "'+file_out+'"')

def decode(media_in,file_ext):
	if ismp3(media_in) or file_ext == 'mp3':
		os.system('mpg123 -q -s "'+media_in+'" -w "'+media_in+'.wav"')
	if isogg(media_in) or file_ext == 'ogg':
		os.system('oggdec -o "'+media_in+'.wav" "'+media_in+'"')
	if isflac(media_in) or file_ext == 'flac':
		os.system('flac -d "'+media_in+'"')
	if iswav(media_in) or file_ext == 'wav':
		os.system('sox "'+media_in+'" -w -r 44100 -t wav -c2 "'+media_in+'.wav"')
	if isaiff(media_in) or file_ext == 'aiff':
		os.system('sox "'+media_in+'" -w -r 44100 -t aiff -c2 "'+media_in+'.wav"')

def normalize(media_in):
	os.system('normalize-audio "'+media_in+'"')

def create_md5_key(dir_in,file_in):
	media_in = dir_in+file_in
	os.system('md5sum -b "'+media_in+'" "'+media_in+'.md5"')

def check_md5_key(dir_in,file_in):
	media_in = dir_in+file_in
	md5_log = os.popen4('md5sum -c "'+media_in+'" "'+media_in+'.md5"')
	if 'OK' in md5_log.split(':'):
		return True
	else:
		return False

def compare_md5_key(file_in,file_out):
	media_in = file_in
	media_out = file_out
	if not os.path.exists(media_in):
		return False
	else:
		print 'Checking md5sums...'
		file_in_in, file_in_out = os.popen4('md5sum -b "'+media_in+'"')
		file_out_in, file_out_out = os.popen4('md5sum -b "'+media_out+'"')
		for line in file_in_out.readlines():
			line = line.split('*')
			line = line[0]
			#print line
			for file_out_out_line in file_out_out.readlines():
				file_out_out_line= file_out_out_line.split('*')
				file_out_out_line= file_out_out_line[0]
				#print file_out_out_line	
				if line == file_out_out_line:
					print 'Files are equal...\n'
					return True
					exit
				else:
					print 'Files are different...\n'
					return False
					exit
		
def create_par_key(dir_in,file_in):
	media_in = dir_in+file_in
	os.system('par2 c -n1 "'+media_in+'"')

def recover_par_key(dir_in):
	for file in os.listdir(dir_in):
		media_in = dir_in+file
		if iswav(media_in):
			os.system('par2 r "'+media_in+'"')

def verify_par_key(media_in):
	os.system('par2 v "'+media_in+'.par2"')

def clean_directory(dir_in,type_list):
	for enc_type in type_list:
		if os.path.exists(dir_in+enc_type):
			print 'Removing '+dir_in+enc_type
			os.system('rm -rf "'+dir_in+enc_type+'"')

def audio_length_sec(file) :
	file_in, file_out = os.popen4('wavinfo "'+file+'" | grep wavDataSize')
	for line in file_out.readlines():
		line_split = line.split(':')
		value = int(int(line_split[1])/(4*44100))
		return value

def ext_is_audio(file):
	file_name_woext, file_ext = tag_tools.filename_split(file)
	return file_ext == "mp3" or file_ext == "ogg" or file_ext == "flac" or file_ext == "wav" or file_ext == "aif" or file_ext == "aiff" or file_ext == "WAV" or file_ext == "AIFF" or file_ext == "AIF" or file_ext == "MP3" or file_ext == "OGG" or file_ext == "FLAC"

def isaudio(file) :
	file_in, file_out = os.popen4('file "'+file+'"')
	for line in file_out.readlines():
		line_split = line.split(' ')
		return (iswav16(file) or iswav(file) or ismp3(file) or isogg(file) or isflac(file) or isaiff(file) or isaiff16(file))

def iswav(file) :
	file_in, file_out = os.popen4('file "'+file+'"')
	for line in file_out.readlines():
		line_split = line.split(' ')
		return ('WAVE' in line_split)

def iswav16(file) :
	file_in, file_out = os.popen4('file "'+file+'"')
	for line in file_out.readlines():
		line_split = line.split(' ')
		return ('WAVE' in line_split) and ('16' in line_split)

def isaiff(file) :
	file_in, file_out = os.popen4('file "'+file+'"')
	for line in file_out.readlines():
		line_split = line.split(' ')
		return ('AIFF' in line_split)

def isaiff16(file) :
	file_in, file_out = os.popen4('file "'+file+'"')
	for line in file_out.readlines():
		line_split = line.split(' ')
		return ('AIFF' in line_split) and ('16' in line_split)

def ismp3(file) :
	file_in, file_out = os.popen4('file "'+file+'"')
	for line in file_out.readlines():
		line_split_space = line.split(' ')
		line_split_comma = line.split(',')
		return (('MPEG' in line_split_space and ' layer III' in line_split_comma) or 'MP3' in line_split_space)

def isogg(file) :
	file_in, file_out = os.popen4('file "'+file+'"')
	for line in file_out.readlines():
		line_split = line.split(',')
		return (' Vorbis audio' in line_split)

def isflac(file) :
	file_in, file_out = os.popen4('file "'+file+'"')
	for line in file_out.readlines():
		line_split = line.split(' ')
		return ('FLAC' in line_split)

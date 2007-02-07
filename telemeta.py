#!/usr/bin/python
# *-* coding: utf-8 *-*
"""
   telemeta

   Copyright (c) 2006-2007 Guillaume Pellerin <yomguy@altern.org>

   This program is free software; you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation; either version 2 of the License, or
   (at your option) any later version.

   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with this program; if not, write to the Free Software
   Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
"""

# Version
# =======
version = '0.2.7'

# Modules and error routines
# ==========================
import os, sys, re, string, shutil
import xml.dom.minidom
import xml.dom.ext
import consts
import audio_marking
import tag_tools
import audio_tools
import default_tags
import default_options
import typeToolBox
from audio_tools import *


# Info, error
# ===========
if len(sys.argv) == 1 :
	print "telemeta v"+str(version)+" (c) 2006 Guillaume Pellerin <yomguy@altern.org>>"
	print "version: "+str(version)
	print "depends: python, python-xml, python-mutagen, sox, oggenc, flac, lame, normalize-audio, ecasound, wavbreaker, festival"
	print "distributed under the terms of the GNU Public License v2.\n"
	print """   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.\n"""
	sys.exit('Type telemeta --help for help !\n')

elif sys.argv[1] == '--help':
	print "TELEMETA:"
	print "         backups, transcodes, tags and marks any audio content with metadata\n"
	print "VERSION:"
	print "         "+str(version)+'\n'
	print "DEPENDS:"
	print "         python, python-xml, python-mutagen, sox, oggenc, flac, lame, normalize-audio, ecasound, wavbreaker, festival\n"
	print "COPYRIGHT:"
	print "         Copyright (c) 2006 Guillaume Pellerin <yomguy@altern.org>\n"
	print "LICENSE:"
	print "         distributed under the terms of the GNU Public License v2.\n"
	print "USAGE:"
	print "         telemeta [OPTIONS] COLLECTION [OPTIONS] [MEDIA] \n"
	print "COLLECTION:"
	print "         - the name of collection you want to create"
	print "         - the name of collection you want to backup or process into\n"
	print "MEDIA:"
	print "         - an audio file"
	print "         - a directory when the --album option is given\n"
	print "OPTIONS:"
	print "         --create       creates a collection repository"
	print "         --backup       backups and transcodes wave files to a collection"
	print "         --album        proccesses an entire directory (one shot album)"
	print "         --from-xml     takes tags and opts in original xml source"
	print "         --force        forces file conversion"
	print "         --add-tag      add a tag to a collection"
	print '         --par2         forces security "par2" key creation'
	print "         --all-default  chooses default argument for all question"
	print '         --recover      check an repair the backuped media with the previously created "par2" security key'
	print "         --rsync        synchronizes a collection with a remote server repository (ssh+rsync)"
	print "         --erase        erases a collection (flac, ogg, mp3 only !)"
	print "         --version      gives the program version"
	print "         --help         gives help page\n"
	print "EXAMPLES:"	
	print "         telemeta --create my_collection"
	print "         telemeta --backup my_collection file.wav"
	print "         telemeta --backup my_collection --album /path/to/directory/"
	print "         telemeta --backup my_collection --album --par2 --rsync /path/to/directory/"
	print "         telemeta --backup my_collection --album --par2 --rsync --force /path/to/directory/\n"
	print "AUTHOR:"
	print "         Guillaume Pellerin <yomguy@altern.org>\n"
	print "URL:"
	print "         http://svn.parisson.org/telemeta\n"
	print 'IMPORTANT:'
	print "         With the '--album' option, it supposed that all your wav files in the directory are named respectively to this scheme :"
	print "            artist-title[-album-date-genre-description][.wav]"
	print "         where the 'artist' and 'title' tags are necessary needed."
	print "         Tags between [] are optional main tags.\n"
	print "FOR MORE INFORMATIONS :"
	print "         - read the README file"
	print "         - go to http://svn.parisson.org/telemeta"
	sys.exit('         - email me !\n')

elif sys.argv[1] == '--version':
	sys.exit('Version: '+str(version))

else :
	print "telemeta v"+str(version)+" (c) 2006 Guillaume Pellerin <yomguy@altern.org>"
	print """   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.\n"""


# Initialisation
# ===============

argv = sys.argv
len_argv = len(argv)

# Get collection consts
collection = consts.Collection()

# Get arguments
if '--recover' in argv :
	index = argv.index('--recover')
	audio_tools.recover_par_key(argv[index+1]+os.sep)
	sys.exit('Directory successfully recovered !')

if '--erase' in argv :
	type_list = tag_tools.get_consts_value('type_list')
	type_list = type_list.split(',')
	index = argv.index('--erase')
	audio_tools.clean_directory(argv[index+1],type_list)
	sys.exit('Media directories successfully cleaned !')

if '--force' in argv :
	print 'Warning: forcing file transfert and conversion (no audio test) !\n'
	mode_force = True
else :
	mode_force = False

if '--album' in argv :
	print 'Warning: album (recusive) mode...\n'
	mode_album = True
else :
	mode_album = False

if '--backup' in argv :
	print 'Warning: backup mode...\n'
	mode_backup = True
else :
	mode_backup = False

if '--tags' in argv :
	print 'Warning: making tags...\n'
	mode_tags = True
else :
	mode_tags = False

if '--add-tag' in argv :
	print 'Warning: adding tags...\n'
	mode_add_tag = True
else :
	mode_add_tag = False

if '--from-xml' in argv :
	print 'Warning: processing from XML...\n'
	mode_from_xml = True
else :
	mode_from_xml = False

if '--clean-strings' in argv :
	print 'Warning: Cleaning strings...\n'
	mode_clean = True
else :
	mode_clean = False

if '--all-default' in argv :
	print 'Warning: default mode enabled...\n'
	mode_default = True
else :
	mode_default = False

if '--par2' in argv :
	print 'Warning: creates par2 security keys...\n'
	mode_par2 = True
else :
	mode_par2 = False

if '--rsync' in argv :
	print 'Warning: synchronize with remote host...\n'
	mode_rsync = True
else :
	mode_rsync = False

if '--create' in argv :
	print 'Warning: creating a telemeta collection...\n'
	mode_create = True
else :
	mode_create = False

# Creates user default dir
user_dir = tag_tools.get_consts_value('user_dir')
if not os.path.exists(user_dir):
	os.mkdir(user_dir)

# Create or check the databse config
default_collection_xml = tag_tools.get_consts_value('default_collection_xml')
if not os.access(default_collection_xml, os.F_OK) :
	tag_tools.write_collection_consts(default_collection_xml)

# Create the collection
if mode_create :
	if len(argv) == 3 :
		index = argv.index('--create')
		collection_name = argv[index+1]
		tag_tools.ask_write_collection(collection_name)
		default_collection_xml = tag_tools.get_consts_value('default_collection_xml')
		collection_dir = tag_tools.get_consts_value('collection_dir')
		if not os.path.exists(collection_dir):
			os.mkdir(collection_dir)
		else :
				sys.exit('ERROR: the collection '+collection_name+' already exists')
		tag_tools.write_collection_consts(default_collection_xml)
		tag_tools.write_collection_consts(collection_dir+os.sep+collection_name+'.xml')
		# Parses collection data
		sys.exit("\nCollection created ! You can now --backup media in it...")
	else :
		sys.exit("ERROR: no collection name given... : give a name for your collection.")
# Backup into the collection
elif mode_backup :
	# Check syntax
	if not os.path.exists(sys.argv[len(sys.argv)-1]) :
		sys.exit("ERROR: no such media... : give a directory or a file as last argument.")
	index = argv.index('--backup')
	collection_name = argv[index+1]
	collection_xml = user_dir+os.sep+collection_name+'.xml'
	if not os.path.exists(collection_xml) :
		sys.exit("This collection doesn't exists. Create it first ! (--create)")
	else :
		doc = xml.dom.minidom.parse(user_dir+os.sep+collection_name+'.xml')
		print "Parsing collection XML file..."
		tag_tools.get_collection_consts(doc)
		collection_dir = tag_tools.get_consts_value('collection_dir')
		print "OK\n"
	

# Creates source dir
src_dir = collection_dir+os.sep+'src'+os.sep
if not os.path.exists(src_dir) :
        os.mkdir(src_dir)

# Creates user default tag/opt file and parse it
default_tag_xml = tag_tools.get_consts_value('default_tag_xml')
if not os.access(default_tag_xml, os.F_OK) :
	tag_tools.write_def_tags(default_tag_xml)

# Parses tag data
doc = xml.dom.minidom.parse(default_tag_xml)
tag_tools.get_def_tags(doc)

# Initializes master file list
file_master_list = range(1)

# File listing for album mode
if mode_album :
	master_dir = argv[len_argv-1]+os.sep
	if os.path.isdir(master_dir):
		file_master_list = os.listdir(master_dir)
	else:
		sys.exit('Please give a directory path for the last argument (album mode)...')
# File listing in normal mode
else :
	master_dir = argv[len_argv-1]
	if os.path.isdir(master_dir):
		file_master_list = os.listdir(master_dir)
	elif os.path.isfile(master_dir):
		master_dir = os.getcwd()+os.sep
		file_master_list[0] = str(argv[len_argv-1])
	else:
		sys.exit('Please give a directory or a file path for the last argument...')

# Asks tags if mode album
if mode_album and not mode_from_xml :
	tag_tools.ask_write_tag()
	tag_tools.write_def_tags(default_tag_xml)


# Main loop
# =========

for file in file_master_list :
	if isaudio(master_dir+os.sep+file) or (mode_force and ext_is_audio(master_dir+os.sep+file)):
		print '\n'
		print '+------------------------------------------------------------------------------------'
		print '| Processing '+master_dir+file
		print '+------------------------------------------------------------------------------------'

		# Init
		file_name = file
		file_in = file
		dir_in = src_dir

		# Backup mode
		if mode_backup :
			album_dir_tmp = tag_tools.get_tag_value('ALBUM')
			album_dir = collection_dir+os.sep+'src'+os.sep+album_dir_tmp+os.sep
			if not os.path.exists(album_dir) :
				os.mkdir(album_dir)
			if isaudio(master_dir+file) and ( not audio_tools.compare_md5_key(master_dir+file,album_dir+file) or mode_force ) :
				print 'Copying files into: '+album_dir+''
				os.system('cp -ra "'+master_dir+file+'" '+album_dir)
				print 'OK\n'
			#else:
			#	sys.exit(master_dir+file+' is not an audio file...')
			src_dir = album_dir
			dir_in = src_dir
		else :
			dir_in = master_dir

		# Creating par2 key
		par_key_value = tag_tools.get_opt_value('par_key')
		if mode_par2 and par_key_value :
			# Creating "par2" security keys
			print 'Creating "par2" security keys...'
			audio_tools.create_par_key(dir_in,file)

		# Name, extension
		file_name_woext, file_ext = tag_tools.filename_split(file)
		tag_tools.add_tag('ORIGINAL_FILENAME',file)
		tag_tools.add_tag('ORIGINAL_TYPE',file_ext)

		# Get original XML
		if mode_from_xml :
			doc = xml.dom.minidom.parse(dir_in+file_name+'.xml')
			tag_tools.get_def_tags(doc)

		# Album mode
		if mode_album :
			# Getting file main tags
			title,artist,file_name_new = tag_tools.name2tag(dir_in,file_name_woext,file_ext)
			tag_tools.add_tag('ARTIST',artist)
			tag_tools.add_tag('TITLE',title)
			print "Artist: "+artist
			print "Title: "+title+'\n'
			#tag_tools.write_def_tags(default_tag_xml)

		# Asks for new metadata and write default user tags/options
		if not mode_default and not mode_from_xml and not mode_album:
			tag_tools.ask_write_tag()
		tag_tools.write_def_tags(default_tag_xml)



		# Clean mode
		if mode_clean :
			file_name = tag_tools.clean_filename(file_name)
			# Renaming backup source file
			tag_tools.rename_file(dir_in,dir_out,file,file_name)

		# Writing xml data
		if not mode_from_xml :
			print 'Writing xml data...'
			tag_tools.write_def_tags(dir_in+file_name+'.xml')

		# Getting encoding types
		enc_types = tag_tools.get_opt_value('enc_types')
		enc_types = string.replace(enc_types,' ','').split(',')

		# Checking existing file
		for enc_type in enc_types:
			dir_out = master_dir+enc_type+os.sep
			file_out = file_name_woext+'.'+enc_type
			if not os.path.exists(dir_out+file_out):
				new_track = True
			else :
				new_track = False

		# Decoding to a new 16 bits wav file if needed
		if not iswav16(dir_in+file_in) and new_track:
			print "Decoding to wav 16 bits..."
			audio_tools.decode(dir_in+file_in,file_ext)
			# Important !
			type_list = tag_tools.get_consts_value('type_list')
			type_list = type_list.split(',')
			if not file_ext in type_list :
				file_in=file_in+'.wav'

		# Normalize file if needed
		normalize_value = tag_tools.get_opt_value('normalize')
		if normalize_value:
			print 'Normalizing...'
			audio_tools.normalize(dir_in+file_in)

		# Marking
		audio_marking_value = tag_tools.get_opt_value('audio_marking')
		auto_audio_marking = tag_tools.get_opt_value('auto_audio_marking')
		audio_marking_file = tag_tools.get_opt_value('audio_marking_file')
		audio_marking_timeline = tag_tools.get_opt_value('audio_marking_timeline')
		audio_marking_timeline = string.replace(audio_marking_timeline,' ','').split(',')
		if audio_marking_value and new_track:
			if auto_audio_marking:
				print 'Creating track audio mark...'
				audio_marking.make_auto_mark(dir_in,file_in)
				audio_marking_file = dir_in+file_in+'_mark.wav'
			print 'Marking '+file_in+' with '+audio_marking_file+'...'
			audio_marking.mark_audio(dir_in,file_in,audio_marking_file,audio_marking_timeline)
			file_in = 'marked_'+file_in

		# Encoding loop
		for enc_type in enc_types:
			dir_out = collection_dir+os.sep+enc_type+os.sep
			if not os.path.exists(dir_out):
				os.mkdir(dir_out)
			album = tag_tools.get_tag_value('ALBUM')
			dir_out = collection_dir+os.sep+enc_type+os.sep+album+os.sep
			if not os.path.exists(dir_out):
				os.mkdir(dir_out)
			file_out = file_name_woext+'.'+enc_type

			if not os.path.exists(dir_out+file_out) or mode_force :
				print 'Converting '+dir_in+file_name+' to '+enc_type+'...'
				# Encoding
				print 'Encoding file...'
				audio_tools.encode(enc_type,dir_in,file_in,dir_out,file_out)
				print 'Writing tags to encoded file...'
				tag_tools.write_tags(enc_type,dir_out,file_out)

			else :
				print dir_out+file_out+' already exists !'
				if mode_tags :
					print 'But writing tags to encoded file...'
					tag_tools.write_tags(enc_type,dir_out,file_out)

		# Remove tmp files
		file_list = os.listdir(src_dir)
		for file in file_list:
			if 'marked_' in file or '.ewf' in file or '_mark.wav' in file or file_ext+'.wav' in file:
				os.system('rm "'+dir_in+file+'"')

	else :
		print file+" is not an audio file !"

# Sync to the remote server
if mode_rsync :
	net_backup_host = tag_tools.get_consts_value('net_backup_host')
	net_backup_dir = tag_tools.get_consts_value('net_backup_dir')
	print '+------------------------------------------------------------------------------------'
	print '| Synchronizing with '+net_backup_host
	print '+------------------------------------------------------------------------------------'
	os.system('rsync -avzLp --delete --rsh="ssh -l '+os.environ["USER"]+'" '+collection_dir+' '+os.environ["USER"]+'@'+net_backup_host+':'+net_backup_dir)
	print "Collection Synchronized !"


# End
# ===

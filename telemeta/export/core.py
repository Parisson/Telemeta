# -*- coding: utf-8 -*-
#
# Copyright (C) 2007 Parisson SARL
# Copyright (c) 2006-2007 Guillaume Pellerin <pellerin@parisson.com>
# All rights reserved.
#
# This software is licensed as described in the file COPYING, which
# yo"u should have received as part of this distribution. The terms
# are also available at http://svn.parisson.org/telemeta/TelemetaLicense.
#
# Author: Guillaume Pellerin <pellerin@parisson.com>

import os
import re
import string

import telemeta.export
from telemeta.export import *
from telemeta.core import *
import xml.dom.minidom
import xml.dom.ext

class ExporterCore(Component):
	"""Defines the main parts of the exporting tools :
	paths, formats, metadata..."""

	def __init__(self):
		self.source = ''
		self.collection = ''
		self.verbose = ''
		self.dest = ''
		self.metadata = []
		self.cache_dir = 'cache'

	def set_cache_dir(self,path):
		self.cache_dir = path

	def normalize(self):
		""" Normalize the source and return its path """
		args = ''
		if self.verbose == '0':
			args = '-q'
		try:
			os.system('normalize-audio '+args+' "'+self.source+'"')
			return self.source
		except IOError:
			return 'Exporter error: Cannot normalize, path does not exist.'

	def check_md5_key(self):
		""" Check if the md5 key is OK and return a boolean """
		try:
			md5_log = os.popen4('md5sum -c "'+self.dest+ \
								'" "'+self.dest+'.md5"')
			return 'OK' in md5_log.split(':')
		except IOError:
			return 'Exporter error: Cannot check the md5 key...'
	
	def get_file_info(self):
		""" Return the list of informations of the dest """
		return self.export.get_file_info()

	def get_wav_length_sec(self) :
		""" Return the length of the audio source file in seconds """
		try:
			file1, file2 = os.popen4('wavinfo "'+self.source+ \
									 '" | grep wavDataSize')
			for line in file2.readlines():
				line_split = line.split(':')
				value = int(int(line_split[1])/(4*44100))
				return value
		except IOError:
			return 'Exporter error: Cannot get the wav length...'

	def compare_md5_key(self):
		""" Compare 2 files wih md5 method """
		in1, in2 = os.popen4('md5sum -b "'+self.source+'"')
		out1, out2 = os.popen4('md5sum -b "'+self.dest+'"')
		for line in in2.readlines():
			line1 = line.split('*')[0]
		for line in out2.readlines():
			line2 = line.split('*')[0]
		return line1 == line2

	def write_metadata_xml(self,path):
		doc = xml.dom.minidom.Document()
		root = doc.createElement('telemeta')
		doc.appendChild(root)
		for tag in self.metadata.keys() :
			value = self.metadata[tag]
			node = doc.createElement(tag)
			node.setAttribute('value', str(value))
			#node.setAttribute('type', get_type(value))
			root.appendChild(node)
		xml_file = open(path, "w")
		xml.dom.ext.PrettyPrint(doc, xml_file)
		xml_file.close()


	def pre_process(self, item_id, source, metadata, ext, cache_dir, options):
		""" Pre processing of the core. Prepare the export path and
		return it"""
		self.item_id = item_id
		self.source = source
		file_name = get_file_name(self.source)
		file_name_wo_ext, file_ext = split_file_name(file_name)
		self.cache_dir = cache_dir
		self.options = options

		self.metadata = metadata
		self.collection = self.metadata['Collection']
		self.artist = self.metadata['Artist']
		self.title = self.metadata['Title']

		# Decode the source if needed
		if os.path.exists(self.source) and not iswav16(self.source):
			# TO FIX !
			self.source = self.export.decode()

		# Normalize if demanded
		if 'normalize' in self.metadata and self.metadata['normalize']:
			self.normalize()

		# Define the cache directory
		self.ext = self.get_file_extension()

		# Define and create the destination path
		# At the moment, the target directory is built with this scheme in
		# the cache directory : ./%Format/%Collection/%Artist/
		self.dest = self.cache_dir
		export_dir = os.path.join(self.ext,self.collection,self.artist)

		if not os.path.exists(os.path.join(self.dest,export_dir)):
			for _dir in export_dir.split(os.sep):
				self.dest = os.path.join(self.dest,_dir)
				if not os.path.exists(self.dest):
					os.mkdir(self.dest)
		else:
			self.dest = os.path.join(self.dest,export_dir)

		# Set the target file
		target_file = file_name_wo_ext+'.'+self.ext
		self.dest = os.path.join(self.dest,target_file)
		return self.dest


	def post_process(self, item_id, source, metadata, ext, cache_dir, options):
		""" Post processing of the Core. Print infos, etc..."""
		if 'verbose' in self.options and self.options['verbose'] != '0':
			print self.dest
			print self.get_file_info()


# External functions

def get_type(value):
	""" Return a String with the type of value """
	types = {bool : 'bool', int : 'int', str : 'str'}
	# 'bool' type must be placed *before* 'int' type, otherwise booleans are
	# detected as integers
	for type in types.keys():
		if isinstance(value, type) :
			return types[type]
	raise TypeError, str(value) + ' has an unsupported type'

def get_cast(value, type) :
	""" Return value, casted into type """
	if type == 'bool' :
		if value == 'True' :
			return True
		return False
	elif type == 'int' :
		return int(value)
	elif type == 'str' :
		return str(value)
	raise TypeError, type + ' is an unsupported type'

def get_file_mime_type(path):
	""" Return the mime type of a file """
	try:
		file_out1, file_out2 = os.popen4('file -i "'+path+'"')
		for line in file_out2.readlines():
			line_split = line.split(': ')
			mime = line_split[len(line_split)-1]
			return mime[:len(mime)-1]
	except IOError:
		return 'Exporter error [1]: path does not exist.'

def get_file_type_desc(path):
	""" Return the type of a file given by the 'file' command """
	try:
		file_out1, file_out2 = os.popen4('file "'+path+'"')
		for line in file_out2.readlines():
			description = line.split(': ')
			description = description[1].split(', ')
			return description
	except IOError:
		return 'Exporter error [1]: path does not exist.'

def iswav(path):
	""" Tell if path is a WAV """
	try:
		mime = get_file_mime_type(path)
		return mime == 'audio/x-wav'
	except IOError:
		return 'Exporter error [1]: path does not exist.'

def iswav16(path):
	""" Tell if path is a 16 bit WAV """
	try:
		file_type_desc = get_file_type_desc(path)
		return iswav(path) and '16 bit' in file_type_desc
	except IOError:
		return 'Exporter error [1]: path does not exist.'

def get_file_name(path):
	""" Return the file name targeted in the path """
	return os.path.split(path)[1]

def split_file_name(file):
	""" Return main file name and its extension """
	try:
		return os.path.splitext(file)
	except IOError:
		return 'Exporter error [1]: path does not exist.'

def clean_word(word) :
	""" Return the word without excessive blank spaces and underscores """
	word = re.sub("^[^\w]+","",word) 	#trim the beginning
	word = re.sub("[^\w]+$","",word) 	#trim the end
	#word = string.replace(word,' ','_')
	word = re.sub("_+","_",word) 		#squeeze continuous _ to one _
	word = re.sub("^[^\w]+","",word) 	#trim the beginning _
	#word = string.capitalize(word)
	return word

def recover_par_key(path):
	""" Recover a file with par2 key """
	os.system('par2 r "'+path+'"')

def verify_par_key(path):
	""" Verify a par2 key """
	os.system('par2 v "'+path+'.par2"')

def get_consts_value(self, data):
	value = self.collection.__dict__[data]
	value_type = getType(value)
	return value, value_type

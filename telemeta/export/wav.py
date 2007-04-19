# -*- coding: utf-8 -*-
#
# Copyright (C) 2007 Parisson SARL
# Copyright (c) 2006-2007 Guillaume Pellerin <pellerin@parisson.com>
# All rights reserved.
#
# This software is licensed as described in the file COPYING, which
# you should have received as part of this distribution. The terms
# are also available at http://svn.parisson.org/telemeta/TelemetaLicense.
#
# Author: Guillaume Pellerin <pellerin@parisson.com>

import os
import string

from telemeta.export.core import *

class WavExporter(ExporterCore):
	"""Defines methods to export to OGG Vorbis"""

	def __init__(self):
		self.item_id = ''
		self.metadata = []
		self.description = ''
		self.info = []
		self.source = ''
		self.dest = ''
		
		
	def get_format(self):
		return 'WAV'
	
	def get_file_extension(self):
		return 'wav'

	def get_mime_type(self):
		return 'audio/x-wav'

	def get_description(self):
		return """S00N"""

	def get_file_info(self):
		try:
			file1, file2 = os.popen4('wavinfo "'+self.dest+'"')
			info = []
			for line in file2.readlines():
				info.append(clean_word(line[:-1]))
			self.info = info
			return self.info
		except IOError:
			return 'Exporter error [1]: file does not exist.'

	def set_cache_dir(self,path):
		"""Set the directory where cached files should be stored. Does nothing
        if the exporter doesn't support caching. 
       
        The driver shouldn't assume that this method will always get called. A
        temporary directory should be used if that's not the case.
        """
		self.cache_dir = path

	def decode(self):
		try:
			file_name, ext = get_file_name(self.source)
			dest = self.cache_dir+os.sep+file_name+'.wav'
			os.system('sox "'+self.source+'" -w -r 44100 -t wav -c2 "'+ \
					  dest+'.wav"')
			self.source = dest
			return dest
		except IOError:
			return 'ExporterError [2]: decoder not compatible.'

	def write_tags(self):
		# Create metadata XML file !
		self.write_metadata_xml(self.dest+'.xml')
	
	def create_md5_key(self):
		""" Create the md5 keys of the dest """
		try:
			os.system('md5sum -b "'+self.dest+'" >"'+self.dest+'.md5"')
		except IOError:
			return 'Exporter error: Cannot create the md5 key...'
	
	def create_par_key(self):
		""" Create the par2 keys of the dest """
		args = 'c -n1 '
		if not 'verbose' in self.metadata or self.metadata['verbose'] == '0':
			args = args + '-q -q '
		try:
			os.system('par2 '+args+' "'+self.dest+'"')
		except IOError:
			return 'Exporter error: Cannot create the par2 key...'

	def process(self, item_id, source, metadata):
		self.item_id = item_id
		self.source = source
		self.metadata = metadata

		try:
			# Pre-proccessing (core)
			self.ext = self.get_file_extension()
			self.dest = self.pre_process(self.item_id,
										 self.source,
										 self.metadata,
										 self.ext,
										 self.cache_dir)

			#if self.compare_md5_key():
			os.system('cp -a "'+self.source+'" "'+ self.dest+'"')
			#print 'COPIED'
			
			# Pre-proccessing (self)
			self.write_tags()
			self.post_process(self.item_id,
						 self.source,
						 self.metadata,
						 self.ext,
						 self.cache_dir)

			# Special post process
			# Create the md5 key
			#if 'md5' in self.metadata and self.metadata['md5']:
			self.create_md5_key()

			# Create the par2 key
			#if 'par2' in self.metadata and self.metadata['par2']:
			self.create_par_key()

			# Output				
			return self.dest

		except IOError:
			return 'ExporterError [3]: source file does not exist.'


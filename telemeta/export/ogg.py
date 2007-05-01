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
from telemeta.export.api import IExporter
from mutagen.oggvorbis import OggVorbis

class OggExporter(ExporterCore):
	"""Defines methods to export to OGG Vorbis"""

	implements(IExporter)
	
	def __init__(self):
		self.item_id = ''
		self.metadata = {}
		self.description = ''
		self.info = []
		self.source = ''
		self.dest = ''
		self.options = {}
		self.bitrate_default = '192'

	def get_format(self):
		return 'OGG'
	
	def get_file_extension(self):
		return 'ogg'

	def get_mime_type(self):
		return 'application/ogg'

	def get_description(self):
		return 'FIXME'

	def get_file_info(self):
		try:
			file_out1, file_out2 = os.popen4('ogginfo "'+self.dest+'"')
			info = []
			for line in file_out2.readlines():
				info.append(clean_word(line[:-1]))
			self.info = info
			return self.info
		except IOError:
			return 'Exporter error [1]: file does not exist.'

	#def set_cache_dir(self,path):
	#	self.cache_dir = path

	def decode(self):
		try:
			os.system('oggdec -o "'+self.cache_dir+os.sep+self.item_id+
					  '.wav" "'+self.source+'"')
			return self.cache_dir+os.sep+self.item_id+'.wav'
		except IOError:
			return 'ExporterError [2]: decoder not compatible.'

	def write_tags(self):
		media = OggVorbis(self.dest)
		for tag in self.metadata.keys():
			media[tag] = str(self.metadata[tag])
		media.save()
		
	def process(self, item_id, source, metadata, options=None):
		self.item_id = item_id
		self.source = source
		self.metadata = metadata
		args = ''
		
		if not options is None:
			self.options = options
			
			if 'verbose' in self.options and self.options['verbose'] != '0':
				args = args
			else:
				args = args + ' -Q '
			
			if 'ogg_bitrate' in self.options:
				args = args + '-b '+self.options['ogg_bitrate']
			elif 'ogg_quality' in self.options:
				args = args + '-q '+self.options['ogg_quality']
			else:
				args = args + '-b '+self.bitrate_default

		else:
			args = ' -Q -b '+self.bitrate_default

		if os.path.exists(self.source) and not iswav16(self.source):
			self.source = self.decode()
			
		try:
			# Pre-proccessing (core)
			self.ext = self.get_file_extension()
			self.dest = self.pre_process(self.item_id,
							self.source,
							self.metadata,
							self.ext,
							self.cache_dir,
							self.options)
			
			# Encoding
			os.system('oggenc '+args+' -o "'+self.dest+
					  '" "'+self.source+'"')
			
			# Pre-proccessing (self)
			self.write_tags()
			self.post_process(self.item_id,
						 self.source,
						 self.metadata,
						 self.ext,
						 self.cache_dir,
						 self.options)
						
			# Output
			return self.dest

		except IOError:
			return 'ExporterError [3]: source file does not exist.'


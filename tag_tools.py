#!/usr/bin/python
# *coding: utf-8*
#
# Copyright (c) 2006 Guillaume Pellerin <pellerin@parisson.com>
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
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301 USAA

import os, sys, re, string
import default_tags
import default_options
import consts
import typeToolBox
import xml.dom.minidom
import xml.dom.ext
from audio_tools import *
from mutagen.flac import FLAC
from mutagen.oggvorbis import OggVorbis
from mutagen.id3 import ID3, TIT2, TP1, TAL, TDA, TCO, COM

# Default values are used at first
tags = default_tags.Tags()
options = default_options.Options()
collection = consts.Collection()

# Collection
# ============

def write_collection_consts(fic):
	doc = xml.dom.minidom.Document()
	root = doc.createElement('telemeta')
	doc.appendChild(root)
	for data in collection.__dict__.keys() :
		value = collection.__dict__[data]
		node = doc.createElement('data')
		node.setAttribute('name', data)
		node.setAttribute('value', str(value))
		node.setAttribute('type', typeToolBox.getType(value))
		root.appendChild(node)
	file_object = open(fic, "w")
	xml.dom.ext.PrettyPrint(doc, file_object)
	file_object.close()

def get_collection_consts(doc):
	for data in doc.documentElement.getElementsByTagName('data') :
		name = data.getAttribute('name')
		value = typeToolBox.cast(data.getAttribute('value'), data.getAttribute('type'))
		collection.__dict__[name] = value

def ask_write_collection(name):
	global collection
	for data in collection.__dict__.keys() :
		if data == 'collection_name' :
			def_value = name
			type_def_value = typeToolBox.getType(def_value)
			value = raw_input(data+' ? ['+str(def_value)+']: ')
		elif data == 'default_collection_xml' :
			collection_xml = '/home/'+os.environ["USER"]+'/.telemeta/'+name+'.xml'
			type_def_collection = typeToolBox.getType(collection_xml)
			collection_tmp = typeToolBox.cast(collection_xml,type_def_collection)
			collection.__dict__[data] = collection_tmp
			value = collection.__dict__[data]
		elif data == 'collection_dir' :
			collection_dir = '/home/'+os.environ["USER"]+'/'+name
			type_def_collection_dir = typeToolBox.getType(collection_dir)
			collection_tmp = typeToolBox.cast(collection_dir,type_def_collection_dir)
			collection.__dict__[data] = collection_tmp
			def_value = collection.__dict__[data]
			value = raw_input(data+' ? ['+str(def_value)+']: ')
		elif data == 'user_dir' :
			def_value = '/home/'+os.environ["USER"]+'/.telemeta/'
			type_def_value = typeToolBox.getType(def_value)
			value = def_value
		elif data == 'default_tag_xml' :
			def_value = '/home/'+os.environ["USER"]+'/.telemeta/default_tags.xml'
			type_def_value = typeToolBox.getType(def_value)
			value = def_value
		else :
			def_value = collection.__dict__[data]
			type_def_value = typeToolBox.getType(def_value)
			value = raw_input(data+' ? ['+str(def_value)+']: ')
		if not value == '' :
			value = typeToolBox.cast(value,type_def_value)
			#value = string.replace(in_float,' ','')
			collection.__dict__[data] = value

def get_consts_value(data):
	value = collection.__dict__[data]
	type_value = typeToolBox.getType(value)
	return value

# TAGS
# =====

def write_tags(enc_type,dir_out,file_out):
	media_out = dir_out+file_out

	if enc_type == 'flac':
		audio = FLAC(media_out)
		for tag in tags.__dict__.keys():
			if tag == 'COMMENT':
				audio['DESCRIPTION'] = tags.__dict__[tag]
			else:
				audio[tag] = tags.__dict__[tag]
		audio.save()

	if enc_type == 'ogg':
		audio = OggVorbis(media_out)
		for tag in tags.__dict__.keys():
			audio[tag] = tags.__dict__[tag]
		audio.save()

	if enc_type == 'mp3':
		audio = ID3(media_out)
		#tags = ['ALBUM','DATE','GENRE','SOURCE','ENCODER','COMMENT']
		tag = tags.__dict__['TITLE']
		audio.add(TIT2(encoding=3, text=tag))
		tag = tags.__dict__['ARTIST']
		audio.add(TP1(encoding=3, text=tag))
		tag = tags.__dict__['ALBUM']
		audio.add(TAL(encoding=3, text=tag))
		tag = tags.__dict__['DATE']
		audio.add(TDA(encoding=3, text=tag))
		tag = tags.__dict__['GENRE']
		audio.add(TCO(encoding=3, text=tag))
		tag = tags.__dict__['COMMENT']
		audio.add(COM(encoding=3, text=tag))
		audio.save()

def write_def_tags(fic):
	doc = xml.dom.minidom.Document()
	root = doc.createElement('telemeta')
	doc.appendChild(root)
	for tag in tags.__dict__.keys() :
		value = tags.__dict__[tag]
		node = doc.createElement('tag')
		node.setAttribute('name', tag)
		node.setAttribute('value', str(value))
		node.setAttribute('type', typeToolBox.getType(value))
		root.appendChild(node)
	for opt in options.__dict__.keys() :
		value = options.__dict__[opt]
		node = doc.createElement('opt')
		node.setAttribute('name', opt)
		node.setAttribute('value', str(value))
		node.setAttribute('type', typeToolBox.getType(value))
		root.appendChild(node)
	file_object = open(fic, "w")
	xml.dom.ext.PrettyPrint(doc, file_object)
	file_object.close()

def ask_write_tag():
	global tags
	global options
	for tag in tags.__dict__.keys() :
		def_value = tags.__dict__[tag]
		type_def_value = typeToolBox.getType(def_value)
		value = raw_input(tag+' ? ['+str(def_value)+']: ')
		if not value == '' :
			value = typeToolBox.cast(value,type_def_value)
			#value = string.replace(in_float,' ','')
			tags.__dict__[tag] = value
	for opt in options.__dict__.keys() :
		def_value = options.__dict__[opt]
		type_def_value = typeToolBox.getType(def_value)
		value = raw_input(opt+' ? ['+str(def_value)+']: ')
		if not value == '' :
			value = typeToolBox.cast(value,type_def_value)
			#value = string.replace(in_float,' ','')
			options.__dict__[opt] = value

def get_def_tags(doc):
	for tag in doc.documentElement.getElementsByTagName('tag') :
		name = tag.getAttribute('name')
		value = typeToolBox.cast(tag.getAttribute('value'), tag.getAttribute('type'))
		tags.__dict__[name] = value
	for opt in doc.documentElement.getElementsByTagName('opt') :
		name = opt.getAttribute('name')
		value = typeToolBox.cast(opt.getAttribute('value'), opt.getAttribute('type'))
		options.__dict__[name] = value

def rename_tag(old_tag,new_tag):
	tag_list = tags.__dict__.keys()
	if old_tag in tag_list:
		tag_index = tag_list.index(old_tag)
		tag_list.remove(old_tag)
		tag_list.insert(tag_index,new_tag)

def get_tag_value(tag):
	value = tags.__dict__[tag]
	type_value = typeToolBox.getType(value)
	return value

def get_opt_value(opt):
	value = options.__dict__[opt]
	type_value = typeToolBox.getType(value)
	return value

def add_tag(tag,value):
	tag_list = tags.__dict__.keys()
	tag_list.insert(0,tag)
	tags.__dict__[tag] = value

def add_opt(opt,value):
	opt_list = options.__dict__.keys()
	opt_list.insert(0,opt)
	options.__dict__[opt] = value

def rename_file(src_dir,file,file_name):
	if (file_name != "" and file_name != file):
		print "Renaming: %s -> %s\n" % (file,file_name)
		os.rename(src_dir+file, src_dir+file_name)

def filename_split(file_name):
	filename_split = file_name.split('.')
	if len(filename_split) > 0:
		file_ext = filename_split[len(filename_split)-1]
	else:
		file_ext = ''
	file_name_woext = '.'.join(filename_split[:-1])
	return file_name_woext, file_ext

#def check_ext():
	#if not ext_is_audio(file):
		#file_name_woext = file_name
		#if iswav(src_dir+file) :
			#file_ext = "wav"
		#if isaiff(src_dir+file) :
			#file_ext = "aiff"
		#if ismp3(src_dir+file) :
			#file_ext = "mp3"
		#if isogg(src_dir+file) :
			#file_ext = "ogg"
		#if isflac(src_dir+file) :
			#file_ext = "flac"

def clean_filename(file_name) :
	file_name = re.sub("^[^\w]+","",filename) #trim the beginning
	file_name = re.sub("[^\w]+$","",file_name) #trim the end
	file_name = string.replace(file_name,' ','_')
	file_name = re.sub("_+","_",file_name) #squeeze continuous _ to one _
	file_name = re.sub("^[^\w]+","",file_name) #trim the beginning _
	#file_name = string.capitalize(file_name)
	return file_name

def name2tag(src_dir,file_name_woext,file_ext):
	# get main tag
	tag_list = file_name_woext.split('-')
	tag_list_new = range(len(tag_list))

	#for num_t in tag_list[0]:
	#	if num_t == str(int(num_t)):
	#		i_t = 1
	#	else:

	# computing main tags if many tags
	if len(tag_list) > 1 :
		i_t = 0
		artist_tmp = string.replace(tag_list[i_t],' ','_')
		artist_tmp = artist_tmp.split('_')
		i = 0
		for artist_word in artist_tmp :
			artist_tmp[i] = string.capitalize(artist_word)
			i = i+1
		artist = '_'.join(artist_tmp[:])
		artist = re.sub("[\_]+$","",artist) #trim the end
		tag_list_new[i_t] = artist
		artist = string.replace(artist,'_',' ')

		i_t = i_t + 1
		title = string.replace(tag_list[i_t],' ','_')
		title = re.sub("^[\_]+","",title) #trim the beginning
		title = re.sub("[\_]+$","",title) #trim the end
		title_tmp = title.split('_')
		title_tmp[0] = string.capitalize(title_tmp[0])
		title = '_'.join(title_tmp[:])
		tag_list_new[i_t] = title
		title = string.replace(title,'_',' ')

	# computing main tag if only one tag
	if len(tag_list) == 1 :
		artist = get_tag_value('ARTIST')
		i_t = 0
		title = string.replace(tag_list[i_t],' ','_')
		title = re.sub("^[\_]+","",title) #trim the beginning
		title = re.sub("[\_]+$","",title) #trim the end
		title_tmp = title.split('_')
		title_tmp[0] = string.capitalize(title_tmp[0])
		title = '_'.join(title_tmp[:])
		tag_list_new[i_t] = title
		title = string.replace(title,'_',' ')

	file_name_new = '-'.join(tag_list_new[:])

	# renaming main source file
	file_name = file_name_new+'.'+file_ext

	return title,artist,file_name_new

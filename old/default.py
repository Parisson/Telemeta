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

class Tags :

    def __init__(self) :
        self.COLLECTION = 'Unknown'
        self.ARTIST = 'Unknown'
        self.TITLE = 'Unknown'
        self.ALBUM = 'Unknown'
        self.GENRE = 'Other'
        self.DATE = '1900'
        self.SOURCE = 'Here'
        self.ENCODER = 'me@domain.com'
        self.COMMENT = 'No comment'
        self.ORIGINAL_MEDIA = '1/4" tape'


class Options :

    def __init__(self) :
        self.collection = 'Unknown'
        self.enc_types = 'flac, ogg, mp3'
        self.ogg_bitrate ='192'
        self.mp3_bitrate = '192'
        self.flac_quality = '5'
        self.audio_marking = False
        self.auto_audio_marking = True
        self.audio_marking_file = '/path/to/file'
        self.audio_marking_timeline = 'b, m, e'
        self.par_key = True
        self.normalize = False


class Collection :

    def __init__(self) :
        self.collection_name = 'telemeta_default'
        self.collection_dir = '/home/'+os.environ["USER"]+'/telemeta_default/'
        self.user_dir = '/home/'+os.environ["USER"]+'/.telemeta/'
        self.default_tag_xml = '/home/'+os.environ["USER"]+ \
                               '/.telemeta/default_tags.xml'
        self.default_collection_xml = '/home/'+os.environ["USER"]+ \
                                      '/.telemeta/default_collection.xml'
        self.tag_table = 'ARTIST,TITLE,ALBUM,DATE,GENRE,SOURCE,ENCODER,COMMENT'
        self.type_list = 'mp3,ogg,flac,wav,aiff'
        self.net_backup_host = 'domain.com'
        self.net_backup_dir = '/home/'+os.environ["USER"]+'/telemeta/'


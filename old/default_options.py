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

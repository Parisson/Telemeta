# -*- coding: utf-8 -*-
#
# Copyright (c) 2012-2013 Guillaume Pellerin <yomguy@parisson.com>

# This file is part of TimeSide.

# TimeSide is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.

# TimeSide is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with TimeSide.  If not, see <http://www.gnu.org/licenses/>.

# Author: Guillaume Pellerin <yomguy@parisson.com>


from telemeta.util.xmltodict2 import *


class AutoFade(object):
    """ Automatically applies a fade in and a fade out trasitions between each segment of a KdenLive session.
        Each video clip needs to be splitted into one video track and an audio one ("Split audio"),
        so that an audio fade in/out is also applied.

        MLT files are also supported.
    """

    def __init__(self, path, audio_frames_out=2, audio_frames_in=1,
                       video_frames_out=3, video_frames_in=3):
        self.audio_frames_in = audio_frames_in
        self.audio_frames_out = audio_frames_out
        self.video_frames_in = video_frames_in
        self.video_frames_out = video_frames_out
        self.path = path
        self.session = xmltodict(self.path)

    def audio_fade_out(self, frame_out):
        child = {'attributes': {u'id': u'fadeout',
        u'in': unicode(int(frame_out)-self.audio_frames_out),
        u'out': unicode(frame_out)},
       'children': [{'attributes': {u'name': u'track'},
         'cdata': '0',
         'name': 'property'},
        {'attributes': {u'name': u'window'},
         'cdata': '75',
         'name': 'property'},
        {'attributes': {u'name': u'max_gain'},
         'cdata': '20dB',
         'name': 'property'},
        {'attributes': {u'name': u'mlt_type'},
         'cdata': 'filter',
         'name': 'property'},
        {'attributes': {u'name': u'mlt_service'},
         'cdata': 'volume',
         'name': 'property'},
        {'attributes': {u'name': u'kdenlive_id'},
         'cdata': 'fadeout',
         'name': 'property'},
        {'attributes': {u'name': u'tag'},
         'cdata': 'volume',
         'name': 'property'},
        {'attributes': {u'name': u'kdenlive_ix'},
         'cdata': '1',
         'name': 'property'},
        {'attributes': {u'name': u'gain'}, 'cdata': '1', 'name': 'property'},
        {'attributes': {u'name': u'end'}, 'cdata': '0', 'name': 'property'}],
       'name': 'filter'}

        return child

    def audio_fade_in(self, frame_in):
        child = {'attributes': {u'id': u'fadein',
        u'in': unicode(frame_in),
        u'out': unicode(int(frame_in)+self.audio_frames_in)},
       'children': [{'attributes': {u'name': u'track'},
         'cdata': '0',
         'name': 'property'},
        {'attributes': {u'name': u'window'},
         'cdata': '75',
         'name': 'property'},
        {'attributes': {u'name': u'max_gain'},
         'cdata': '20dB',
         'name': 'property'},
        {'attributes': {u'name': u'mlt_type'},
         'cdata': 'filter',
         'name': 'property'},
        {'attributes': {u'name': u'mlt_service'},
         'cdata': 'volume',
         'name': 'property'},
        {'attributes': {u'name': u'kdenlive_id'},
         'cdata': 'fadein',
         'name': 'property'},
        {'attributes': {u'name': u'tag'},
         'cdata': 'volume',
         'name': 'property'},
        {'attributes': {u'name': u'kdenlive_ix'},
         'cdata': '1',
         'name': 'property'},
        {'attributes': {u'name': u'gain'}, 'cdata': '0', 'name': 'property'},
        {'attributes': {u'name': u'end'}, 'cdata': '1', 'name': 'property'}],
       'name': 'filter'}

        return child


    def video_fade_out(self, frame_out):
        child = {'attributes': {u'id': u'fade_to_black',
        u'in': unicode(int(frame_out)-self.video_frames_out),
        u'out': unicode(frame_out)},
       'children': [{'attributes': {u'name': u'track'},
         'cdata': '0',
         'name': 'property'},
        {'attributes': {u'name': u'start'}, 'cdata': '1', 'name': 'property'},
        {'attributes': {u'name': u'mlt_type'},
         'cdata': 'filter',
         'name': 'property'},
        {'attributes': {u'name': u'mlt_service'},
         'cdata': 'brightness',
         'name': 'property'},
        {'attributes': {u'name': u'kdenlive_id'},
         'cdata': 'fade_to_black',
         'name': 'property'},
        {'attributes': {u'name': u'tag'},
         'cdata': 'brightness',
         'name': 'property'},
        {'attributes': {u'name': u'kdenlive_ix'},
         'cdata': '1',
         'name': 'property'},
        {'attributes': {u'name': u'end'}, 'cdata': '0', 'name': 'property'}],
       'name': 'filter'}

        return child


    def video_fade_in(self, frame_in):
        child = {'attributes': {u'id': u'fade_from_black',
        u'in': unicode(frame_in),
        u'out': unicode(int(frame_in)+self.video_frames_in)},
       'children': [{'attributes': {u'name': u'track'},
         'cdata': '0',
         'name': 'property'},
        {'attributes': {u'name': u'start'}, 'cdata': '0', 'name': 'property'},
        {'attributes': {u'name': u'mlt_type'},
         'cdata': 'filter',
         'name': 'property'},
        {'attributes': {u'name': u'mlt_service'},
         'cdata': 'brightness',
         'name': 'property'},
        {'attributes': {u'name': u'kdenlive_id'},
         'cdata': 'fade_from_black',
         'name': 'property'},
        {'attributes': {u'name': u'tag'},
         'cdata': 'brightness',
         'name': 'property'},
        {'attributes': {u'name': u'kdenlive_ix'},
         'cdata': '1',
         'name': 'property'},
        {'attributes': {u'name': u'end'}, 'cdata': '1', 'name': 'property'}],
       'name': 'filter'}

        return child

    def run(self):
        audio_count = 0
        video_count = 0
        
        for attr in self.session['children']:
            if 'playlist' in attr['name'] and 'children' in attr:
                for att in attr['children']:
                    if 'producer' in att['attributes'] and not 'children' in att:                        
                        producer = att['attributes']['producer']
                        if producer != 'black':
                        
                            frame_in = att['attributes']['in']
                            frame_out = att['attributes']['out']

                            if 'audio' in producer:
                                if not audio_count % 2:
                                    att['children'] = [self.audio_fade_out(frame_out)]
                                else:
                                    att['children'] = [self.audio_fade_in(frame_in)]
                                audio_count += 1


                            if 'video' in producer:
                                if not video_count % 2:
                                    att['children'] = [self.video_fade_out(frame_out)]
                                else:
                                    att['children'] = [self.video_fade_in(frame_in)]
                                video_count += 1

        return dicttoxml(self.session).encode('utf-8')



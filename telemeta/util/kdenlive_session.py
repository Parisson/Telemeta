# -*- coding: utf-8 -*-
# Copyright (C) 2012-2013 Parisson SARL

# This file is part of Telemeta.

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# Authors: Guillaume Pellerin <yomguy@parisson.com>


import time
from telemeta.util.xmltodict2 import *


class KDEnLiveSession(object):

    def __init__(self, path):
        self.session = xmltodict(path)

    def entries(self):
        entries = []
        for attr in self.session['children']:
            if 'playlist' in attr['name'] and 'children' in attr:
                for att in attr['children']:
                    if 'entry' in att['name'] and att['attributes']['producer'] != 'black':
                        entries.append(att['attributes'])
        return entries

    def video_entries(self):
        entries = []
        for attr in self.session['children']:
            if 'playlist' in attr['name'] and 'children' in attr:
                for att in attr['children']:
                    if 'entry' in att['name'] and att['attributes']['producer'] != 'black' \
                            and not 'audio' in att['attributes']['producer']:
                        entries.append(att['attributes'])
        return entries

    def entries_sorted(self):
        return sorted(self.entries(), key=lambda k: int(k['in']), reverse=False)

    def entries_video_seconds(self):
        fps = float(self.profile()['frame_rate_num'])
        list = []
        entries = self.video_entries()
        for i in range(0,len(entries)):
            id = entries[i]['producer'].split('_')[0]
            t_in = int(entries[i]['in'])/fps
            t_out = int(entries[i]['out'])/fps

            if i == 0:
                t = 0
            else:
                t = list[i-1]['t'] + int(entries[i-1]['out'])/fps - int(entries[i-1]['in'])/fps

            list.append({'id' : id, 't': t, 'in': t_in , 'out': t_out })

        return list

    def cuts(self, entries):
        i = 0
        cuts = [0, ]
        for entry in entries:
            if i > 0:
                cuts.append(cuts[i-1] + int(entries[i]['in'])-int(entries[i-1]['out']))
            i += 1
        return cuts

    def first_video_frame(self):
        return int(self.entries_sorted()[0]['in'])

    def profile(self):
        for attr in self.session['children']:
            if 'profile' in attr['name']:
                return attr['attributes']

    def fix_text(self, text):
        try:
            s = text.split(' ')
            i = int(s[1])
            s.insert(2, ':')
            return ' '.join(s)
        except:
            return text

    def markers(self, offset=0, from_first_marker=False):
        """ by default return a dict of markers with timecodes relative to an origin

            if from_first_marker=False: the origin is the first entry timecode
            if from_first_marker=True: the origin is the first entry timecode before the first marker

            offset: general origin offset
        """

        abs_time = 0
        markers = []
        i = 0
        entries = self.entries_video_seconds()

        for attr in self.session['children']:
            if 'kdenlivedoc' in attr['name']:

                for att in attr['children']:
                    if 'markers' in att['name'] and 'children' in att.keys():

                        for at in att['children']:
                            if 'marker' in at['name']:

                                marker_time = float(at['attributes']['time'].replace(',','.'))
                                id = at['attributes']['id']
                                rel_time = 0

                                for entry in entries:
                                    if marker_time >= entry['in'] and marker_time <= entry['out'] and id == entry['id']:
                                        if i == 0 and from_first_marker:
                                            abs_time = entry['t']
                                        rel_time = entry['t'] + (marker_time - entry['in']) - abs_time + offset
                                        break

                                at['attributes']['time'] = rel_time
                                at['attributes']['session_timecode'] = time.strftime('%H:%M:%S', time.gmtime(rel_time))
                                at['attributes']['comment'] = self.fix_text(at['attributes']['comment'])
                                markers.append(at['attributes'])

                            i += 1
        return markers


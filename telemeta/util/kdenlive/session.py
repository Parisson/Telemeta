# -*- coding: utf-8 -*-
# Copyright (C) 2012-2013 Parisson SARL

# This software is a computer program whose purpose is to backup, analyse,
# transcode and stream any audio content with its metadata over a web frontend.

# This software is governed by the CeCILL  license under French law and
# abiding by the rules of distribution of free software.  You can  use,
# modify and/ or redistribute the software under the terms of the CeCILL
# license as circulated by CEA, CNRS and INRIA at the following URL
# "http://www.cecill.info".

# As a counterpart to the access to the source code and  rights to copy,
# modify and redistribute granted by the license, users are provided only
# with a limited warranty  and the software's author,  the holder of the
# economic rights,  and the successive licensors  have only  limited
# liability.

# In this respect, the user's attention is drawn to the risks associated
# with loading,  using,  modifying and/or developing or reproducing the
# software by the user in light of its specific status of free software,
# that may mean  that it is complicated to manipulate,  and  that  also
# therefore means  that it is reserved for developers  and  experienced
# professionals having in-depth computer knowledge. Users are therefore
# encouraged to load and test the software's suitability as regards their
# requirements in conditions enabling the security of their systems and/or
# data to be ensured and,  more generally, to use and operate it in the
# same conditions as regards security.

# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL license and that you accept its terms.

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


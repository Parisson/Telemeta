# -*- coding: utf-8 -*-

import os, re, urllib


class URLMediaParser(object):

    formats = ['mp3', 'wav', 'ogg', 'flac', 'aac', 'mp4', 'webm']

    def __init__(self, url):
        self.url = url
        self.formats = self.get_formats()
        self.urls = []
        if self.url[-1] != '/':
        	self.url += '/'

    def get_formats(self):
    	formats = []
    	for f in self.formats:
    		formats.append(f.upper())
    		formats.append(f.lower())
    		formats.append(f.capitalize())
    	return formats

    def get_urls(self):    
        data = urllib.urlopen(self.url).read()
        for line in data.split("\012"):
            s = re.compile('href=".*\.*"').search(line,1)
            if s:
                filename = line[s.start():s.end()].split('"')[1]
                name, ext = os.path.splitext(filename)
                if ext[1:] in self.formats:
                    self.urls.append(self.url + filename)
        return self.urls


if __name__ == "__main__":
	import sys
	parser = URLMediaParser(sys.argv[-1])
	urls = parser.get_urls()
	print urls
	print len(urls)
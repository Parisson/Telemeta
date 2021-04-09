from optparse import make_option
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from telemeta.models import *
import datetime, time, calendar, itertools
import numpy as np


SECOND = 1
MINUTE = SECOND * 60
HOUR = MINUTE * 60
DAY = HOUR * 24
MONTH = DAY * 30


class Command(BaseCommand):

    help = "log items from the NYUAD project"

    option_list = BaseCommand.option_list + (
          make_option('-l', '--logfile',
            dest='log_file',
            help='log file'),
    )


    year = 2019
    month = 11
    day = 11
    username = 'nyuad'
    items = []

    def process(self, item):
        if item.file and item.code:
            print(item.id)
            self.log.write(item.collection.code + '/' + item.code + '\n')

    def handle(self, *args, **kwargs):
        self.log = open(kwargs['log_file'], 'w')
        current_date = datetime.datetime(self.year, self.month, self.day)
        pub_date = datetime.date(self.year-51, self.month, self.day)

        self.pub_items = MediaItem.objects.filter(
            recorded_from_date__lte=pub_date, 
            file__isnull=False, code__isnull=False)

        revisions = Revision.objects.filter(element_type='item', time__lte=current_date)
        revisions_ids = [revision.element_id for revision in revisions]
 
        for item in self.pub_items:
            if item.id in revisions_ids:
                self.items.append(item)

        user = User.objects.get(username=self.username)
        playlists = Playlist.objects.filter(author=user)

        for playlist in playlists:
            for resource in playlist.resources.all():
                if resource.resource_type == 'item':
                    item = MediaItem.objects.get(id=resource.resource_id)
                    if item.recorded_from_date:
                        if item.recorded_from_date <= pub_date:
                            if not item in self.items:
                                self.items.append(item)
                elif resource.resource_type == 'collection':
                    collection = MediaCollection.objects.get(id=resource.resource_id)
                    for item in collection.items.all():
                        if item.recorded_from_date:
                            if item.recorded_from_date <= pub_date:
                                if not item in self.items:
                                    self.items.append(item)

	for item in self.items:
            self.process(item)
        
        print(len(self.items))
        self.log.close()


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
    username = nyuad


    def process(self, item, log):
        log.write(item.collection.code + '/' + item.code + '\n')

    def handle(self, *args, **kwargs):
        log = open(kwargs['log_file'], 'w')
        limit_date = datetime.datetime(self.year-51, self.month, self.day)

        pub_items = MediaItem.objects.filter(recorded_from_date__lte=limit_date).select_related('collection')

        for item in pub_items:
            self.process(item, log)

        user = User.objects.get(username=self.username)
        playlists = playlists.objects.filter(user=user)

        for playlist in playlists:
            for resource in playlist.resources.all():
                if resource.resource_type == 'item':
                    item = MediaItem.objects.get(id=resource.resource_id)
                    self.process(item, log)
                elif resource.resource_type == 'collection':
                    collection = MediaCollection.objects.get(id=resource.resource_id)
                    for item in collection.items.all():
                        self.process(item, log)

        log.close()


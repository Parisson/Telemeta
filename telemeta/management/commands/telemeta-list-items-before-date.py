from optparse import make_option
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from telemeta.models import *
import datetime, time, calendar, itertools
import numpy as np


SECOND = 1
MINUTE = SECOND * 60
HOUR = MINUTE * 60
DAY = HOUR * 24
MONTH = DAY * 30


class Command(BaseCommand):
    help = "log items created before a given date"

    option_list = BaseCommand.option_list + (
          make_option('-y', '--year',
            dest='year',
            help='year of the first revision'),
          make_option('-m', '--month',
            dest='month',
            help='month of the first revision'),
          make_option('-d', '--day',
            dest='day',
            help='day of the first revision'),
          make_option('-l', '--logfile',
            dest='log_file',
            help='log file'),
    )

    def handle(self, *args, **kwargs):
        log_file = open(kwargs['log_file'], 'w')
        limit_date = datetime.datetime(int(kwargs.get('year')), int(kwargs.get('month')), int(kwargs.get('day')))
        revisions = Revision.objects.filter(element_type='item', time__lte=limit_date, change_type='creation')
        for revision in revisions:
            item = MediaItem.objects.get(id=revision.element_id)
            log_file.write(item.code)
        log_file.close()


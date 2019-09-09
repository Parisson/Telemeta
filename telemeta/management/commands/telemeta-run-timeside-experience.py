from optparse import make_option
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.core.exceptions import MultipleObjectsReturned

import os

from telemeta.models import MediaItem, MediaCollection

import timeside.core
from timeside.server.models import *
from timeside.server.models import _PENDING, _DONE
from timeside.core.tools.test_samples import generateSamples
import simplejson as json


class Command(BaseCommand):
    help = "Run a list of timeside plugins on all telemeta items"

    media_root = os.path.normpath(settings.MEDIA_ROOT)
    processor_blacklist = []

    def add_arguments(self, parser):
        parser.add_argument('-s', '--selection_title',
                            dest='selection_title',
                            help='define the title of the selection')

        parser.add_argument('-e', '--experience_title',
                            dest='experience_title',
                            help='define the title of the experience')

        parser.add_argument('-m', '--media_directory',
                            dest='media_directory',
                            help='define the media directory')

        parser.add_argument('-l', '--log',
                            dest='log',
                            help='define log file')

        parser.add_argument('-f', '--force',
                            action='store_true',
                            dest='force',
                            help='Force overwrite data')

        parser.add_argument('-c', '--cleanup',
                            action='store_true',
                            dest='cleanup',
                            help='Cleanup result data')

        parser.add_argument('-t', '--test',
                            action='store_true',
                            dest='test',
                            help='test mode')

        parser.add_argument('-p', '--pid',
                            nargs='+',
                            type=str,
                            help='Processor ID')

        parser.add_argument('-cc', '--collection_code',
                            dest='collection_code',
                            help='define the telemeta collection code')

    def create_selection(self):
        if self.collection_code:
            if not self.selection_title:
                selection_title = self.collection_code
            else:
                selection_title = self.selection_title
            collection = MediaCollection.objects.get(code=self.collection_code)
            tm_items = collection.items.all()
        else:
            selection_title = self.selection_title
            tm_items = MediaItem.objects.all()

        self.selection, c = Selection.objects.get_or_create(title=selection_title)
        items = self.selection.items.all()

        provider, c  = Provider.objects.get_or_create(pid='telemeta_crem')

        for tm_item in tm_items:
            if tm_item.file:
                path = tm_item.file.path
                item, c = Item.objects.get_or_create(title=tm_item.title,
                                                     source_file=path,
                                                     external_id=tm_item.code,
                                                     external_uri=tm_item.get_url(),
                                                     provider=provider)
                if not item in items:
                    self.selection.items.add(item)

                if self.cleanup:
                    for result in item.results.all():
                        result.delete()

    def create_experience(self):
        presets = []

        processors = timeside.core.processor.processors(timeside.core.api.IProcessor)
        for proc in processors:
            trig = True
            # print(proc.id())
            if proc.id() in self.pid:
                for processor in self.processor_blacklist:
                    if processor in proc.id():
                        trig = False
                if trig:
                    processor, c = Processor.objects.get_or_create(pid=proc.id())
                    try:
                        preset, c = Preset.objects.get_or_create(processor=processor, parameters='{}')
                        presets.append(preset)
                    except Preset.MultipleObjectsReturned:
                        print(Preset.objects.filter(processor=processor, parameters='{}'))

        if self.experience_title:
            self.experience, c = Experience.objects.get_or_create(title=self.experience_title)
        else:
            self.experience = Experience()
            self.experience.save()
        for preset in presets:
            if not preset in self.experience.presets.all():
                self.experience.presets.add(preset)

    def handle(self, *args, **options):
        self.selection_title = options.get('selection_title')
        self.experience_title = options.get('experience_title')
        self.media_directory =  options.get('media_directory')
        self.force = options.get('force')
        self.test = options.get('test')
        self.cleanup = options.get('cleanup')
        self.pid = options.get('pid')
        self.collection_code = options.get('collection_code')

        self.create_selection()
        print('number of items: ', self.selection.items.all().count())

        self.create_experience()
        print('processors: ', self.pid)

        task, c = Task.objects.get_or_create(experience=self.experience, selection=self.selection)
        if c or task.status != _DONE or self.force:
            task.status = _PENDING
            task.save()



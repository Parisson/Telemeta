from optparse import make_option
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

import os
import timeside.core
from timeside.core.tools.test_samples import generateSamples
from telemeta.models import *


class Command(BaseCommand):
    help = "Setup and run a boilerplate for testing"
    cleanup =  True
    code = 'Tests'

    def processor_cleanup(self):
        for processor in Processor.objects.all():
            processor.delete()

    def result_cleanup(self):
        for result in Result.objects.all():
            result.delete()

    def handle(self, *args, **options):
        collections = MediaCollection.objects.filter(code=self.code)
        if collections:
            collection = collections[0]
            created = False
        else:
            collection = MediaCollection(title=self.code, code=self.code, public_access='full')
            created = True
            collection.save()

        #TS# selection, created = Selection.objects.get_or_create(title='Tests')
        

        if created:
            #TS#presets = []
            #TS#blacklist =['decoder', 'live', 'gain', 'vamp']
            #TS#processors = timeside.core.processor.processors(timeside.core.api.IProcessor)
            #TS#for proc in processors:
            #TS#    trig = True
            #TS#    for black in blacklist:
            #TS#        if black in proc.id():
            #TS#            trig = False
            #TS#    if trig:
            #TS#        processor, c = Processor.objects.get_or_create(pid=proc.id())
            #TS#        preset, c = Preset.objects.get_or_create(processor=processor, parameters='{}')
            #TS#        presets.append(preset)

            media_dir = 'items' + os.sep + 'tests'
            samples_dir = settings.MEDIA_ROOT + media_dir
            samples = generateSamples(samples_dir=samples_dir)

            for sample in samples.iteritems():
                filename, path = sample
                title = os.path.splitext(filename)[0]
                path = media_dir + os.sep + filename
                #TS#item, c = Item.objects.get_or_create(title=title, file=path)
                #TS#if not item in selection.items.all():
                #TS#    selection.items.add(item)
                #TS#if self.cleanup:
                #TS#    for result in item.results.all():
                #TS#        result.delete()
                mediaitem, c = MediaItem.objects.get_or_create(title=title,
                                    code=self.code + '-' + slugify(filename),
                                    file=path, collection=collection, public_access = 'full')
            #TS# 
            #TS# experience, c = Experience.objects.get_or_create(title='All')
            #TS# for preset in presets:
            #TS#     if not preset in experience.presets.all():
            #TS#         experience.presets.add(preset)
            #TS# 
            #TS# task = Task(experience=experience, selection=selection)
            #TS#  task.save()

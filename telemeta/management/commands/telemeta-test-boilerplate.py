from optparse import make_option
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

import os
from telemeta.models import *
from timeside.core.tools.test_samples import generateSamples


class Command(BaseCommand):
    help = "Setup and run a boilerplate for testing"

    code = 'Tests'

    def handle(self, *args, **options):
        # NOT for production
        # self.processor_cleanup()
        # self.result_cleanup()

        media_dir = 'items' + os.sep + 'tests'
        samples_dir = settings.MEDIA_ROOT + media_dir
        samples = generateSamples(samples_dir=samples_dir)

        collection, c = MediaCollection.objects.get_or_create(title=self.code,
                            code=self.code)

        for sample in samples.iteritems():
            filename, path = sample
            title = os.path.splitext(filename)[0]
            path = media_dir + os.sep + filename
            item, c = MediaItem.objects.get_or_create(title=title,
                                    code=self.code + '-' + slugify(filename),
                                    file=path, collection=collection)


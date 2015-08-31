from optparse import make_option
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

import os
import timeside.core
from timeside.server.models import *
from timeside.core.tools.test_samples import generateSamples
from telemeta.models import *
from telemeta.views.epub import *


class Command(BaseCommand):
    help = "Export all collections of a corpus and itself to EPUB3 files in cache"

    def handle(self, *args, **options):
        corpus_id = args[-1]
        corpus = MediaCorpus.objects.get(public_id=corpus_id)
        book = BaseEpubMixin()
        book.write_book(corpus)
        for collection in corpus.children.all():
            book = BaseEpubMixin()
            book.write_book(corpus, collection=collection)

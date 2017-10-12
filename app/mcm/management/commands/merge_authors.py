# -*- coding: utf-8 -*

from django.core.management.base import BaseCommand, CommandError
from django.db.utils import IntegrityError

import os
import logging
import tempfile

from mcm.models import Author, AuthorRole

DOUBLONS = {
    1077406: 667506,
    992606: 783806,
    1075006: 765506,
    2074706: 1712906,
    2083606: 634406,
    1075606: 458906,
    1075706: 459006,
    1059406: 653206,
    1076806: 645706,
    463906: 440406,
    1073906: 755006,
    1072306: 583506,
    1057206: 491206,
    1057406: 491406,
    2349106: 1559906,
    1059106: 617106,
    1027706: 623506,
    1057306: 491306,
    1088206: 644406,
    1914806: 1914706,
    585406: 584806,
    599006: 598506,
    610006: 609606,
    1941506: 1940706,
    1062806: 775606,
    1323706: 1319206,
    2106206: 1279006,
    2227006: 612106,
    1064206: 609306,
    1064306: 609506,
    1751706: 1609306,
    1943306: 1346606}


class Command(BaseCommand):
    help = 'Remove Doublons in Authors'

    # def add_arguments(self, parser):
    #    parser.add_argument('xml_file', type=str, default='data/exports/Auteurs_clean.xml')

    def handle(self, *args, **options):
        for del_old_id, keep_old_id in DOUBLONS.items():
            try:
                author_to_delete = Author.objects.get(old_id=del_old_id)
            except Author.DoesNotExist:
                print "Author %d already deleted" % del_old_id
                continue
            author_to_keep = Author.objects.get(old_id=keep_old_id)
            roles = AuthorRole.objects.filter(author_id=author_to_delete)
            for role in roles:
                print "Replace author %d by author %d for doc %s" % (author_to_delete.old_id,
                                                                     author_to_keep.old_id,
                                                                     role.document.__str__())
                role.author = author_to_keep
                role.save()
            author_to_delete.delete()

from django.core.management.base import BaseCommand, CommandError
from django.db.models import Count

from ...models import Document
from ...models import Author
from ...models import Notice


class Command(BaseCommand):
    help = 'Import items from XML'

    def handle(self, *args, **options):

        duplicate = Notice.objects.values('code').annotate(Count('id')).order_by().filter(id__count__gt=1)

        for item in duplicate:
            code = item['code']
            docs = Notice.objects.filter(code=code)
            print ('-----------')
            print('code %s' % code)
            for doc in docs:
                print('\t Doc old id : %s' % doc.old_id)
                print('\t Doc title : %s' % doc.title)

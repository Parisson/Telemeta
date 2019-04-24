from optparse import make_option
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.utils import translation

from telemeta.models import Playlist, MediaCollection, MediaItem
from telemeta.views.item import ItemView
import os


class Command(BaseCommand):
    help = "Export media files from playlists of a given user"
    args = "username"

    def handle(self, *args, **options):
        username = args[0]
        extension = args[1]
        title_keyword = args[2]
        log_file_empty = '/srv/media/log/' + username + '_playlist_empty_items.log'
        log_file_full = '/srv/media/log/' + username + '_playlist_full_items.log'

        user = User.objects.get(username=username)
        playlists = user.playlists.filter(title__icontains=title_keyword)
        items = []
        view = ItemView()

        for playlist in playlists:
            print(playlist.title.encode('utf-8'))
            resources = playlist.resources.all()
            for resource in resources:
                if resource.resource_type == 'collection':
                    collection = MediaCollection.objects.get(id=resource.resource_id)
                    for item in collection.items.all():
                        items.append(item)
                elif resource.resource_type == 'item':
                    item = MediaItem.objects.get(id=resource.resource_id)
                    items.append(item)

        os.remove(log_file_empty)
        os.remove(log_file_full)
        log_empty = open(log_file_empty, 'w')
        log_full = open(log_file_full, 'w')
        medias = os.listdir('/srv/media/export')
        print('number of items: ', len(items))

        for item in items:
            if item.code:
                code = item.code
            else:
                code = item.old_code

            if not item.file:
                log_empty.write(code + '\n')
            else:
                filename = item.code + '.mp3'
                if not filename in medias:
                    view.item_transcode(item, extension)
                    log_full.write(code + '\n')

        log_empty.close()
        log_full.close()

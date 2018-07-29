from optparse import make_option
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.utils import translation

from telemeta.models import Playlist, MediaCollection, MediaItem
from telemeta.views.item import ItemView


class Command(BaseCommand):
    help = "Export media files from playlists of a given user"
    args = "username"

    def handle(self, *args, **options):
        username = args[0]
        extension = args[1]

        user = User.objects.get(username=username)
        playlists = user.playlists.all()
        items = []
        view = ItemView()

        for playlist in playlists:
            resources = playlist.resources.all()
            for resource in resources:
                if resource.resource_type == 'collection':
                    collection = MediaCollection.objects.get(id=resource.resource_id)
                    for item in collection.items.all():
                        items.append(item)
                elif resource.resource_type == 'item':
                    item = MediaItem.objects.get(id=resource.resource_id)
                    items.append(item)

        for item in items:
            view.item_transcode(item, extension)

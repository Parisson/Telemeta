from telemeta.models.media import *
from telemeta.models.instrument import *
from telemeta.models.system import User
from django.contrib import admin

admin.site.register(MediaCollection)
admin.site.register(MediaItem)
admin.site.register(MediaPart)
admin.site.register(Playlist)
admin.site.register(PlaylistResource)
admin.site.register(Instrument)


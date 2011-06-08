from telemeta.models.media import *
from telemeta.models.instrument import *
from telemeta.models.location import *
from django.contrib import admin


class MediaCollectionAdmin(admin.ModelAdmin):
    search_fields = ['title', 'code']
    ordering = ['code']

class MediaItemAdmin(admin.ModelAdmin):
    search_fields = ['title', 'code']
    ordering = ['code']
    exclude = ('copied_from_item', )

class MediaPartAdmin(admin.ModelAdmin):
    search_fields = ['title', 'item__code']
    ordering = ['title']

class InstrumentAdmin(admin.ModelAdmin):
    search_fields = ['name']
    ordering = ['name']
    
class InstrumentAliasAdmin(admin.ModelAdmin):
    search_fields = ['name']
    ordering = ['name']

class InstrumentRelationAdmin(admin.ModelAdmin):
    search_fields = ['instrument__name', 'parent_instrument__name']
    ordering = ['parent_instrument__name']
     
class InstrumentAliasRelationAdmin(admin.ModelAdmin):
    search_fields = ['alias__name', 'instrument__name']
    ordering = ['alias__name']

class LocationAdmin(admin.ModelAdmin):
    search_fields = ['name']
    ordering = ['name']
     
class LocationAliasAdmin(admin.ModelAdmin):
    search_fields = ['location__name', 'alias']
    ordering = ['alias']
     
class LocationRelationAdmin(admin.ModelAdmin):
    search_fields = ['location__name', 'ancestor_location__name']
    ordering = ['ancestor_location__name']

admin.site.register(MediaCollection, MediaCollectionAdmin)
admin.site.register(MediaItem, MediaItemAdmin)
admin.site.register(MediaPart, MediaPartAdmin)

admin.site.register(Instrument, InstrumentAdmin)
admin.site.register(InstrumentAlias, InstrumentAliasAdmin)
admin.site.register(InstrumentRelation, InstrumentRelationAdmin)
admin.site.register(InstrumentAliasRelation, InstrumentAliasRelationAdmin)

admin.site.register(Location, LocationAdmin)
#admin.site.register(LocationType)
admin.site.register(LocationAlias, LocationAliasAdmin)
admin.site.register(LocationRelation, LocationRelationAdmin)


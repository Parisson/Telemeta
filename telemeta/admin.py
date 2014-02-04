# -*- coding: utf-8 -*-
from telemeta.models.media import *
from telemeta.models.instrument import *
from telemeta.models.location import *
from telemeta.models.language import *
from telemeta.models.system import *
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

admin.site.unregister(User)

class MediaFondsAdmin(admin.ModelAdmin):
    search_fields = ['title', 'code']
    ordering = ['code']
    filter_horizontal = ['children']

class MediaCorpusAdmin(admin.ModelAdmin):
    search_fields = ['title', 'code']
    ordering = ['code']
    filter_horizontal = ['children']

class MediaCollectionRelatedInline(admin.StackedInline):
    model = MediaCollectionRelated

class MediaCollectionAdmin(admin.ModelAdmin):
    search_fields = ['title', 'code']
    ordering = ['code']
    inlines = [MediaCollectionRelatedInline]

class MediaItemRelatedInline(admin.StackedInline):
    model = MediaItemRelated

class MediaItemMarkerInline(admin.StackedInline):
    model = MediaItemMarker

class MediaItemTranscodedInline(admin.StackedInline):
    model = MediaItemTranscoded

class MediaItemAdmin(admin.ModelAdmin):
    search_fields = ['title', 'code']
    ordering = ['code']
    exclude = ('copied_from_item', )
    inlines = [MediaItemRelatedInline, 
                MediaItemTranscodedInline,
                MediaItemMarkerInline]

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

class LanguageAdmin(admin.ModelAdmin):
    search_fields = ['name', 'identifier']
    ordering = ['name']

class RevisionAdmin(admin.ModelAdmin):
    search_fields = ['element_id', 'user']
    ordering = ['-time']

class FormatAdmin(admin.ModelAdmin):
    search_fields = ['original_code', 'tape_reference']

class UserProfileInline(admin.StackedInline):
	model = UserProfile

class UserProfileAdmin(UserAdmin):
	inlines = [UserProfileInline]

admin.site.register(MediaFonds, MediaFondsAdmin)
admin.site.register(MediaCorpus, MediaCorpusAdmin)
admin.site.register(MediaCollection, MediaCollectionAdmin)
admin.site.register(MediaItem, MediaItemAdmin)
admin.site.register(MediaPart, MediaPartAdmin)

admin.site.register(Instrument, InstrumentAdmin)
admin.site.register(InstrumentAlias, InstrumentAliasAdmin)
admin.site.register(InstrumentRelation, InstrumentRelationAdmin)
admin.site.register(InstrumentAliasRelation, InstrumentAliasRelationAdmin)

admin.site.register(Location, LocationAdmin)
admin.site.register(LocationType)
admin.site.register(LocationAlias, LocationAliasAdmin)
admin.site.register(LocationRelation, LocationRelationAdmin)

admin.site.register(Language, LanguageAdmin)

admin.site.register(Revision, RevisionAdmin)

admin.site.register(Format, FormatAdmin)

admin.site.register(User, UserProfileAdmin)

admin.site.register(PublisherCollection)
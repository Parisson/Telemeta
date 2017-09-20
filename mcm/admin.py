from django.contrib import admin

# Register your models here.
from .models import Author, Role, AuthorRole
from .models import Reference
from .models import Event, EventEdition, EventType, EventVenue
from .models import GeographicalClassification
from .models import Document
from .models import Notice, Disc, Video, VideoFile, BookThesis, Journal
from .models import Photo, PosterBooklet, Object


class AuthorRoleInline(admin.TabularInline):
    model = AuthorRole
    extra = 1


class AuthorAdmin(admin.ModelAdmin):
    list_filter = ('name', 'old_id')
    search_fields = ['name', 'old_id']
    ordering = ['name']
    inlines = (AuthorRoleInline,)


class ReferenceAdmin(admin.ModelAdmin):
    list_filter = ('name',)
    search_fields = ['name']
    ordering = ['name']


class EventAdmin(admin.ModelAdmin):
    list_filter = ('name',)
    search_fields = ['name']
    ordering = ['name']


class EventTypeAdmin(admin.ModelAdmin):
    list_filter = ('name',)
    search_fields = ['name']
    ordering = ['name']


class EventVenueAdmin(admin.ModelAdmin):
    list_filter = ('name',)
    search_fields = ['name']
    ordering = ['name']


class GeoAdmin(admin.ModelAdmin):
    list_filter = ('name',)
    search_fields = ['name']
    ordering = ['name']


class DocumentAdmin(admin.ModelAdmin):
    list_display = ('code', 'title')
    list_filter = ('code', 'title')
    search_fields = ['title', 'code']
    filter_horizontal = ('keywords', 'related')
    inlines = (AuthorRoleInline,)


class EventEditionAdmin(admin.ModelAdmin):
    list_display = ('event', 'edition')
    ordering = ['event', 'edition']


admin.site.register(Author, AuthorAdmin)
admin.site.register(Reference, ReferenceAdmin)

admin.site.register(Event, EventAdmin)
admin.site.register(EventEdition, EventEditionAdmin)
admin.site.register(EventType, EventTypeAdmin)
admin.site.register(EventVenue, EventVenueAdmin)
admin.site.register(GeographicalClassification, GeoAdmin)

# admin.site.register(Document)
admin.site.register(Notice, DocumentAdmin)
admin.site.register(Disc, DocumentAdmin)
admin.site.register(Video, DocumentAdmin)
admin.site.register(VideoFile, DocumentAdmin)
admin.site.register(BookThesis, DocumentAdmin)
admin.site.register(Journal, DocumentAdmin)
admin.site.register(Photo, DocumentAdmin)
admin.site.register(PosterBooklet, DocumentAdmin)
admin.site.register(Object, DocumentAdmin)

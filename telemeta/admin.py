from django.contrib import admin
from telemeta.models import MediaCollection, MediaItem, MediaPart, MediaCore 
from django import forms

class MediaCoreAdminForm(forms.ModelForm):
    def clean(self):
        data = forms.ModelForm.clean(self)
        id = None
        if data.has_key("id"):
            id = data["id"] = data["id"].strip()
        if not id:
            raise forms.ValidationError(u"id field is required")
        if not MediaCore.is_well_formed_id(id):
            raise forms.ValidationError(u"'%s' is not a well-formed id" % id)
        return data

class MediaCollectionAdminForm(MediaCoreAdminForm):
    class Meta:
        model = MediaCollection
  
class MediaItemAdminForm(MediaCoreAdminForm):
    class Meta:
        model = MediaItem
  
class MediaCollectionAdmin(admin.ModelAdmin):
    form = MediaCollectionAdminForm

class MediaItemAdmin(admin.ModelAdmin):
    form = MediaItemAdminForm

admin.site.register(MediaCollection, MediaCollectionAdmin)
admin.site.register(MediaItem, MediaItemAdmin)
admin.site.register(MediaPart)

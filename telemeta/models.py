import telemeta
from django.db import models
from django.core import validators

class Collection(models.Model):
    "Group related media items"

    name = models.CharField(maxlength=250)

    def __str__(self):
        return self.name

    class Admin:
        pass

class MediaItem(models.Model):
    "Describe an audio/video item with metadata" 

    collection = models.ForeignKey(Collection)
    title = models.CharField(maxlength=250)
    author = models.CharField(maxlength=250)



    def get_dynamic_properties(self):
        "Retrieve dynamic properties associated with a given media item"

        definitions = MediaItemPropertyDefinition.objects.all()
        assigned = MediaItemProperty.objects.filter(media_item=self)
        assigned_dict = {}
        for p in assigned:
            assigned_dict[p.definition.id] = p

        properties = []
        for d in definitions:
            enumeration = MediaItemPropertyEnumerationItem.objects.filter(definition=d)

            if d.id in assigned_dict:
                if d.type == "text":
                    value = assigned_dict[d.id].value
                else:
                    value = assigned_dict[d.id].enum_item

                properties.append({
                    "id": d.id, "name": d.name, "value": value,
                    "type" : d.type, "enumeration" : enumeration})
            else:
                properties.append({"id": d.id, "name": d.name, "value": "", 
                    "type" : d.type, "enumeration" : enumeration})

        return properties

    def __str__(self):
        return self.author + " - " + self.title

    class Meta:
        pass

    class Admin:
        pass

class MediaItemPropertyDefinition(models.Model):
    "Define a media item dynamic property"

    TYPE_CHOICES = (
        ('text', 'Text'),
        ('enumeration', 'Enumeration'),
    ) 

    name = models.CharField(maxlength=64)
    type = models.CharField(maxlength=64, choices = TYPE_CHOICES)

    def __str__(self):
        return self.name

    class Admin:
        pass

class MediaItemPropertyEnumerationItem(models.Model):
    "Define a possible value for media item dynamic enumeration properties"

    definition = models.ForeignKey(MediaItemPropertyDefinition, core=True)
    name = models.CharField(maxlength=250)

    def __str__(self):
        return self.definition.name + " / " + self.name

    class Admin:
        pass
    
class MediaItemProperty(models.Model):
    "Associate a value to a media item dynamic property"

    definition = models.ForeignKey(MediaItemPropertyDefinition, core=True)
    media_item = models.ForeignKey(MediaItem)
    value = models.CharField(maxlength=250)
    enum_item = models.ForeignKey(MediaItemPropertyEnumerationItem, null=True)

    def __str__(self):
        return str(self.media_item) + " / " + str(self.definition)

    class Meta:
        unique_together = (("media_item", "definition"),)

    class Admin:
        pass
  

class Part:
    media_item = models.ForeignKey(MediaItem)
    parent = models.ForeignKey('self', null=True, related_name='children')
    name = models.CharField(maxlength=250)

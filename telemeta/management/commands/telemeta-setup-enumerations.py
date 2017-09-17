from optparse import make_option
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
import telemeta
from telemeta.models.enum import Enumeration, EnumerationProperty


class Command(BaseCommand):
    help = """Create all EnumerationProperty against the Enumeration list"""

    def handle(self, *args, **options):
        from django.db.models import get_models
        models = get_models(telemeta.models)
        for model in models:
            if issubclass(model, Enumeration):
                enumeration_property = EnumerationProperty.objects.filter(enumeration_name=model._meta.module_name)
                if not enumeration_property:
                    enumeration_property = EnumerationProperty(enumeration_name=model._meta.module_name)
                    enumeration_property.is_admin = True
                    enumeration_property.is_hidden = False
                    enumeration_property.save()

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import telemeta.models.fields


def copy_dates(apps, schema_editor):
    Collection = apps.get_model('telemeta','mediacollection')
    for collection in Collection.objects.all():
        collection.recorded_from_year_old = collection.recorded_from_year
        collection.recorded_to_year_old = collection.recorded_to_year
        collection.save()


class Migration(migrations.Migration):

    dependencies = [
        ('telemeta', '0006_mediaitem_mshs_domain'),
    ]

    operations = [
        migrations.AddField(
            model_name='mediacollection',
            name='recorded_from_year_old',
            field=telemeta.models.fields.IntegerField(default=None, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='mediacollection',
            name='recorded_to_year_old',
            field=telemeta.models.fields.IntegerField(default=None, null=True, blank=True),
        ),
        migrations.RunPython(copy_dates),
        # migrations.AlterField(
        #     model_name='mediacollection',
        #     name='recorded_from_year',
        #     field=telemeta.models.fields.DateField(default=None, null=True, verbose_name='recording date (from)', blank=True),
        # ),
        # migrations.AlterField(
        #     model_name='mediacollection',
        #     name='recorded_to_year',
        #     field=telemeta.models.fields.DateField(default=None, null=True, verbose_name='recording date (until)', blank=True),
        # ),
    ]

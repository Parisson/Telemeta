# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import telemeta.models.fields


def integer_to_dates(apps, schema_editor):
    Collection = apps.get_model('telemeta','mediacollection')
    for collection in Collection.objects.all():

        if collection.recorded_from_year_old > 0 :
            collection.recorded_from_year = str(collection.recorded_from_year_old)+'-01-01'
        else :
            collection.recorded_from_year= None

        if collection.recorded_to_year_old > 0 :
            collection.recorded_to_year = str( collection.recorded_to_year_old)+'-12-31'
        else :
            collection.recorded_to_year = None

        collection.save()


class Migration(migrations.Migration):

    dependencies = [
        ('telemeta', '0007_auto_20171207_1004'),
    ]

    operations = [
        migrations.RemoveField(
             model_name='mediacollection',
             name='recorded_from_year',
        ),
        migrations.RemoveField(
            model_name='mediacollection',
            name='recorded_to_year',
        ),
        migrations.AddField(
            model_name='mediacollection',
            name='recorded_from_year',
            field=telemeta.models.fields.DateField(default=None, null=True, verbose_name='recording date (from)', blank=True),
        ),
        migrations.AddField(
            model_name='mediacollection',
            name='recorded_to_year',
            field=telemeta.models.fields.DateField(default=None, null=True, verbose_name='recording date (until)', blank=True),
        ),
        migrations.RunPython(integer_to_dates),
        migrations.RemoveField(
             model_name='mediacollection',
             name='recorded_from_year_old',
        ),
        migrations.RemoveField(
            model_name='mediacollection',
            name='recorded_to_year_old',
        ),
    ]

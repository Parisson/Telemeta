# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import telemeta.models.fields
import dirtyfields.dirtyfields


class Migration(migrations.Migration):

    dependencies = [
        ('telemeta', '0005_auto_20170919_1521'),
    ]

    operations = [
        migrations.CreateModel(
            name='EnumerationProperty',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('enumeration_name', models.CharField(max_length=255, verbose_name='enumeration name')),
                ('is_hidden', telemeta.models.fields.BooleanField(default=False, verbose_name='is hidden')),
                ('is_admin', telemeta.models.fields.BooleanField(default=True, verbose_name='is admin')),
            ],
            options={
                'verbose_name': 'enumeration property',
                'verbose_name_plural': 'enumeration properties',
            },
            bases=(models.Model, dirtyfields.dirtyfields.DirtyFieldsMixin),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mcm', '0032_auto_20171013_1600'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookthesis',
            name='collection_num',
            field=models.CharField(max_length=191, verbose_name='collection number', blank=True),
        ),
        migrations.AlterField(
            model_name='disc',
            name='collection_num',
            field=models.CharField(max_length=191, verbose_name='collection number', blank=True),
        ),
        migrations.AlterField(
            model_name='journal',
            name='collection_num',
            field=models.CharField(max_length=191, verbose_name='collection number', blank=True),
        ),
        migrations.AlterField(
            model_name='video',
            name='collection_num',
            field=models.CharField(max_length=191, verbose_name='collection number', blank=True),
        ),
    ]

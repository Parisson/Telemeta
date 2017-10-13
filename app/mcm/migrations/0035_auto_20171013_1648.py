# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mcm', '0034_auto_20171013_1624'),
    ]

    operations = [
        migrations.AlterField(
            model_name='disc',
            name='duration',
            field=models.CharField(max_length=191, verbose_name='duration', blank=True),
        ),
        migrations.AlterField(
            model_name='video',
            name='duration',
            field=models.CharField(max_length=191, verbose_name='duration', blank=True),
        ),
        migrations.AlterField(
            model_name='videofile',
            name='duration',
            field=models.CharField(max_length=191, verbose_name='duration', blank=True),
        ),
    ]

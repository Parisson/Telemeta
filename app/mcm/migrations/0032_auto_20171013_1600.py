# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mcm', '0031_auto_20171013_1549'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookthesis',
            name='format',
            field=models.TextField(verbose_name='format', blank=True),
        ),
        migrations.AlterField(
            model_name='photo',
            name='format',
            field=models.TextField(verbose_name='format', blank=True),
        ),
        migrations.AlterField(
            model_name='posterbooklet',
            name='format',
            field=models.TextField(verbose_name='format', blank=True),
        ),
    ]

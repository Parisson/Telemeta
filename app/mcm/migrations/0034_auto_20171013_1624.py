# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mcm', '0033_auto_20171013_1617'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookthesis',
            name='format',
            field=models.TextField(null=True, verbose_name='format', blank=True),
        ),
        migrations.AlterField(
            model_name='journal',
            name='format',
            field=models.TextField(null=True, verbose_name='format', blank=True),
        ),
        migrations.AlterField(
            model_name='photo',
            name='format',
            field=models.TextField(null=True, verbose_name='format', blank=True),
        ),
        migrations.AlterField(
            model_name='posterbooklet',
            name='format',
            field=models.TextField(null=True, verbose_name='format', blank=True),
        ),
    ]

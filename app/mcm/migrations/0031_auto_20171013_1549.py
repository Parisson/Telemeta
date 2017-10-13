# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mcm', '0030_auto_20171013_1541'),
    ]

    operations = [
        migrations.AlterField(
            model_name='journal',
            name='format',
            field=models.TextField(verbose_name='format', blank=True),
        ),
    ]

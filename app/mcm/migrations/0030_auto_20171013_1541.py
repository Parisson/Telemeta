# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mcm', '0029_auto_20171013_1533'),
    ]

    operations = [
        migrations.AlterField(
            model_name='journal',
            name='format',
            field=models.CharField(max_length=100, verbose_name='format', blank=True),
        ),
    ]

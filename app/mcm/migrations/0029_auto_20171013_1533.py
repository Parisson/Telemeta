# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mcm', '0028_auto_20171013_1528'),
    ]

    operations = [
        migrations.AlterField(
            model_name='journal',
            name='volume',
            field=models.CharField(max_length=50, verbose_name='volume', blank=True),
        ),
    ]

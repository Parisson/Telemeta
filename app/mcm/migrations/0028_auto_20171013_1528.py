# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mcm', '0027_auto_20171013_1502'),
    ]

    operations = [
        migrations.AlterField(
            model_name='journal',
            name='number',
            field=models.CharField(max_length=50, verbose_name='num\xe9ro de revue', blank=True),
        ),
    ]

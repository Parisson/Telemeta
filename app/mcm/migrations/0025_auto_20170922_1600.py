# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mcm', '0024_auto_20170922_1558'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='object',
            name='collection',
        ),
        migrations.AddField(
            model_name='object',
            name='collection',
            field=models.ForeignKey(verbose_name='collection', blank=True, to='mcm.Collection', null=True),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mcm', '0025_auto_20171013_1354'),
    ]

    operations = [
        migrations.AddField(
            model_name='videofile',
            name='language',
            field=models.ManyToManyField(to='mcm.Language', verbose_name='language'),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('telemeta', '0004_auto_20171205_1114'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mediacollection',
            name='location',
            field=models.ManyToManyField(related_name='locations', null=True, verbose_name='location', to='telemeta.Location', blank=True),
        ),
    ]

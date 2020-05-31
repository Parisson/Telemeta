# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('telemeta', '0012_auto_20200531_0822'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mediaitem',
            name='collector2',
        ),
        migrations.DeleteModel(
            name='Authority',
        ),
    ]

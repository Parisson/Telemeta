# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('telemeta', '0008_auto_20200531_0733'),
    ]

    operations = [
        migrations.RenameField(
            model_name='mediaitem',
            old_name='authority',
            new_name='collector2',
        ),
    ]

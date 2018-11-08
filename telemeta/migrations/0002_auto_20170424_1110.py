# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('telemeta', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='mediaitem',
            options={'verbose_name': 'item', 'permissions': (('can_play_all_items', 'Can play all media items'), ('can_download_all_items', 'Can download all media items'), ('can_run_analysis', 'Can run analysis'))},
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('telemeta', '0010_auto_20200531_0811'),
    ]

    operations = [
        migrations.AddField(
            model_name='authority',
            name='isni',
            field=models.PositiveIntegerField(help_text='International Standard Name Identifier', null=True, verbose_name='isni', blank=True),
        ),
    ]

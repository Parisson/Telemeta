# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('telemeta', '0009_auto_20200531_0805'),
    ]

    operations = [
        migrations.AddField(
            model_name='authority',
            name='biography',
            field=models.TextField(null=True, verbose_name='biography', blank=True),
        ),
        migrations.AddField(
            model_name='authority',
            name='birth',
            field=models.DateField(help_text='YYYY-MM-DD', null=True, verbose_name='birth', blank=True),
        ),
        migrations.AddField(
            model_name='authority',
            name='death',
            field=models.DateField(help_text='YYYY-MM-DD', null=True, verbose_name='death', blank=True),
        ),
    ]

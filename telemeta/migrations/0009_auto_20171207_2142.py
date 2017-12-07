# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('telemeta', '0008_auto_20171207_1349'),
    ]

    operations = [
        migrations.AddField(
            model_name='mediaitem',
            name='informer',
            field=models.ManyToManyField(related_name='item_informers', null=True, verbose_name='informers', to='telemeta.Authority', blank=True),
        ),
        migrations.AddField(
            model_name='mediaitem',
            name='language_iso',
            field=models.ManyToManyField(related_name='item_language', null=True, verbose_name='Language (ISO norm)', to='telemeta.Language', blank=True),
        ),
        #migrations.RemoveField(
        #    model_name='mediaitem',
        #    name='collector',
        #),
        migrations.AddField(
            model_name='mediaitem',
            name='collector',
            field=models.ManyToManyField(related_name='item_collectors', null=True, verbose_name='collectors', to='telemeta.Authority', blank=True),
        ),
    ]

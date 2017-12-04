# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import markdownx.models
import telemeta.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('telemeta', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='mediafonds',
            name='acquisition_mode',
            field=telemeta.models.fields.ForeignKey(related_name='fonds', default=None, blank=True, to='telemeta.AcquisitionMode', null=True, verbose_name='mode of acquisition'),
        ),
        migrations.AddField(
            model_name='mediafonds',
            name='comment',
            field=markdownx.models.MarkdownxField(verbose_name='comment', blank=True),
        ),
        migrations.AddField(
            model_name='mediafonds',
            name='conservation_site',
            field=telemeta.models.fields.CharField(default=b'', max_length=250, verbose_name='conservation site', blank=True),
        ),
    ]

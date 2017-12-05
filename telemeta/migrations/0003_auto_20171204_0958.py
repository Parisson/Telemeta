# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import markdownx.models
import telemeta.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('telemeta', '0002_auto_20171204_0814'),
    ]

    operations = [
        migrations.AddField(
            model_name='mediacorpus',
            name='code_partner',
            field=telemeta.models.fields.CharField(default=b'', max_length=250, verbose_name='code partner', blank=True),
        ),
        migrations.AddField(
            model_name='mediacorpus',
            name='documentation_extra',
            field=markdownx.models.MarkdownxField(verbose_name='documentation extra', blank=True),
        ),
    ]

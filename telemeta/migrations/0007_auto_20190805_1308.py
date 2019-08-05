# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import telemeta.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('telemeta', '0006_enumerationproperty'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mediaitem',
            name='moda_execut',
            field=telemeta.models.fields.CharField(default=b'', max_length=250, verbose_name='perfomance modality', blank=True),
        ),
    ]

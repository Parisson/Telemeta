# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import telemeta.models.fields
import telemeta.models.resource
import dirtyfields.dirtyfields


class Migration(migrations.Migration):

    dependencies = [
        ('telemeta', '0004_auto_20170718_1540'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mediacorpus',
            name='code',
            field=models.CharField(unique=True, max_length=250, verbose_name='code', validators=[telemeta.models.resource.is_valid_resource_code]),
        ),
        migrations.AlterField(
            model_name='mediafonds',
            name='code',
            field=models.CharField(unique=True, max_length=250, verbose_name='code', validators=[telemeta.models.resource.is_valid_resource_code]),
        ),
    ]

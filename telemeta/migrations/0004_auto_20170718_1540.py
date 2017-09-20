# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import telemeta.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('telemeta', '0003_auto_20170718_1502'),
    ]

    operations = [
        migrations.AlterField(
            model_name='format',
            name='original_channels',
            field=telemeta.models.fields.ForeignKey(related_name='format', on_delete=django.db.models.deletion.SET_NULL, default=None, blank=True, to='telemeta.NumberOfChannels', null=True, verbose_name='number of channels'),
        ),
        migrations.AlterField(
            model_name='format',
            name='physical_format',
            field=telemeta.models.fields.ForeignKey(related_name='format', on_delete=django.db.models.deletion.SET_NULL, default=None, blank=True, to='telemeta.PhysicalFormat', null=True, verbose_name='physical format'),
        ),
        migrations.AlterField(
            model_name='format',
            name='tape_speed',
            field=telemeta.models.fields.ForeignKey(related_name='format', on_delete=django.db.models.deletion.SET_NULL, default=None, blank=True, to='telemeta.TapeSpeed', null=True, verbose_name='tape speed (cm/s)'),
        ),
        migrations.AlterField(
            model_name='format',
            name='tape_vendor',
            field=telemeta.models.fields.ForeignKey(related_name='format', on_delete=django.db.models.deletion.SET_NULL, default=None, blank=True, to='telemeta.TapeVendor', null=True, verbose_name='tape vendor'),
        ),
        migrations.AlterField(
            model_name='format',
            name='tape_wheel_diameter',
            field=telemeta.models.fields.ForeignKey(related_name='format', on_delete=django.db.models.deletion.SET_NULL, default=None, blank=True, to='telemeta.TapeWheelDiameter', null=True, verbose_name='tape wheel diameter (cm)'),
        ),
        migrations.AlterField(
            model_name='location',
            name='current_location',
            field=telemeta.models.fields.ForeignKey(related_name='past_names', on_delete=django.db.models.deletion.SET_NULL, default=None, blank=True, to='telemeta.Location', null=True, verbose_name='current location'),
        ),
    ]

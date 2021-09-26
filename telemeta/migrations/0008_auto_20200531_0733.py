# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import telemeta.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('telemeta', '0007_auto_20190505_1749'),
    ]

    operations = [
        migrations.CreateModel(
            name='Authority',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(max_length=50, verbose_name='firstname')),
                ('last_name', models.CharField(max_length=50, verbose_name='lastname')),
            ],
            options={
                'db_table': 'media_authority',
                'verbose_name': 'authority',
            },
        ),
        migrations.AddField(
            model_name='mediaitem',
            name='authority',
            field=telemeta.models.fields.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, default=None, blank=True, to='telemeta.Authority', null=True),
        ),
    ]

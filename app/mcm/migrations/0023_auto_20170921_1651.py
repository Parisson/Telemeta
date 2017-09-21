# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mcm', '0022_auto_20170921_1510'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='title',
            field=models.TextField(verbose_name='title'),
        ),
    ]

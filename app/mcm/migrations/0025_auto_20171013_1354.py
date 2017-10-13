# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mcm', '0024_auto_20171013_1342'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookthesis',
            name='collection',
            field=models.ForeignKey(verbose_name='collection', blank=True, to='mcm.Collection', null=True),
        ),
        migrations.AddField(
            model_name='bookthesis',
            name='language',
            field=models.ManyToManyField(to='mcm.Language', verbose_name='language'),
        ),
        migrations.AddField(
            model_name='disc',
            name='collection',
            field=models.ForeignKey(verbose_name='collection', blank=True, to='mcm.Collection', null=True),
        ),
        migrations.AddField(
            model_name='disc',
            name='language',
            field=models.ManyToManyField(to='mcm.Language', verbose_name='language'),
        ),
        migrations.AddField(
            model_name='journal',
            name='collection',
            field=models.ForeignKey(verbose_name='collection', blank=True, to='mcm.Collection', null=True),
        ),
        migrations.AddField(
            model_name='journal',
            name='language',
            field=models.ManyToManyField(to='mcm.Language', verbose_name='language'),
        ),
        migrations.AddField(
            model_name='video',
            name='collection',
            field=models.ForeignKey(verbose_name='collection', blank=True, to='mcm.Collection', null=True),
        ),
        migrations.AddField(
            model_name='video',
            name='language',
            field=models.ManyToManyField(to='mcm.Language', verbose_name='language'),
        ),
    ]

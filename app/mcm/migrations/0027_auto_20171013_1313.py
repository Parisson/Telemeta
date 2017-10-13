# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mcm', '0026_auto_20171013_1310'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='isedited',
            name='collection',
        ),
        migrations.RemoveField(
            model_name='isedited',
            name='language',
        ),
        migrations.AddField(
            model_name='bookthesis',
            name='collection',
            field=models.ForeignKey(verbose_name='collection', blank=True, to='mcm.Collection', null=True),
        ),
        migrations.AddField(
            model_name='bookthesis',
            name='collection_num',
            field=models.CharField(max_length=50, verbose_name='collection number', blank=True),
        ),
        migrations.AddField(
            model_name='bookthesis',
            name='companion',
            field=models.CharField(max_length=50, verbose_name="mat\xe9riel d'accompagnement", blank=True),
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
            name='collection_num',
            field=models.CharField(max_length=50, verbose_name='collection number', blank=True),
        ),
        migrations.AddField(
            model_name='disc',
            name='companion',
            field=models.CharField(max_length=50, verbose_name="mat\xe9riel d'accompagnement", blank=True),
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
            name='collection_num',
            field=models.CharField(max_length=50, verbose_name='collection number', blank=True),
        ),
        migrations.AddField(
            model_name='journal',
            name='companion',
            field=models.CharField(max_length=50, verbose_name="mat\xe9riel d'accompagnement", blank=True),
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
            name='collection_num',
            field=models.CharField(max_length=50, verbose_name='collection number', blank=True),
        ),
        migrations.AddField(
            model_name='video',
            name='companion',
            field=models.CharField(max_length=50, verbose_name="mat\xe9riel d'accompagnement", blank=True),
        ),
        migrations.AddField(
            model_name='video',
            name='language',
            field=models.ManyToManyField(to='mcm.Language', verbose_name='language'),
        ),
        migrations.DeleteModel(
            name='isEdited',
        ),
    ]

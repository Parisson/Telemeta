# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mcm', '0021_auto_20170913_1200'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='alias',
            field=models.CharField(default='', max_length=191, blank=True),
        ),
        migrations.AlterField(
            model_name='author',
            name='name',
            field=models.CharField(max_length=191, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='collection',
            name='name',
            field=models.CharField(max_length=191, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='document',
            name='code',
            field=models.CharField(max_length=191, verbose_name='code', blank=True),
        ),
        migrations.AlterField(
            model_name='document',
            name='copyright_text',
            field=models.CharField(default='', max_length=191, verbose_name='copyright'),
        ),
        migrations.AlterField(
            model_name='document',
            name='title',
            field=models.CharField(max_length=191, verbose_name='title'),
        ),
        migrations.AlterField(
            model_name='editeddocument',
            name='edition_place',
            field=models.CharField(max_length=191, verbose_name='edition_place'),
        ),
        migrations.AlterField(
            model_name='event',
            name='name',
            field=models.CharField(max_length=191, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='eventtype',
            name='name',
            field=models.CharField(max_length=191, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='eventvenue',
            name='name',
            field=models.CharField(max_length=191, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='geographicalclassification',
            name='name',
            field=models.CharField(max_length=191, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='image',
            name='copyright',
            field=models.CharField(max_length=191, verbose_name='copyright'),
        ),
        migrations.AlterField(
            model_name='image',
            name='name',
            field=models.CharField(max_length=191, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='language',
            name='name',
            field=models.CharField(max_length=191, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='notice',
            name='doc_source',
            field=models.CharField(max_length=191, verbose_name='document source', blank=True),
        ),
        migrations.AlterField(
            model_name='notice',
            name='indexation_date_text',
            field=models.CharField(max_length=191, verbose_name='indexation date', blank=True),
        ),
        migrations.AlterField(
            model_name='notice',
            name='release_date_text',
            field=models.CharField(max_length=191, verbose_name='release date', blank=True),
        ),
        migrations.AlterField(
            model_name='photo',
            name='archive_dvd',
            field=models.CharField(max_length=191, verbose_name='DVD archive'),
        ),
        migrations.AlterField(
            model_name='reference',
            name='name',
            field=models.CharField(max_length=191, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='role',
            name='label',
            field=models.CharField(max_length=191, verbose_name='title', blank=True),
        ),
    ]

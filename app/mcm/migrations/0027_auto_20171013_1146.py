# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mcm', '0026_auto_20171012_1533'),
    ]

    operations = [
        migrations.CreateModel(
            name='Captation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=191, verbose_name='name')),
            ],
            options={
                'verbose_name': 'type de captation',
            },
        ),
        migrations.CreateModel(
            name='Classification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=191, verbose_name='name')),
            ],
            options={
                'verbose_name': 'classification th\xe9matique',
            },
        ),
        migrations.CreateModel(
            name='EditionPlace',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=191, verbose_name='name')),
            ],
            options={
                'verbose_name': "lieu d'\xe9dition",
            },
        ),
        migrations.RemoveField(
            model_name='editeddocument',
            name='collection',
        ),
        migrations.RemoveField(
            model_name='editeddocument',
            name='document_ptr',
        ),
        migrations.RemoveField(
            model_name='editeddocument',
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
            name='format',
            field=models.CharField(max_length=50, verbose_name='format', blank=True),
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
            name='format',
            field=models.CharField(max_length=50, verbose_name='format', blank=True),
        ),
        migrations.AddField(
            model_name='journal',
            name='language',
            field=models.ManyToManyField(to='mcm.Language', verbose_name='language'),
        ),
        migrations.AddField(
            model_name='journal',
            name='number',
            field=models.CharField(max_length=10, verbose_name='num\xe9ro de revue', blank=True),
        ),
        migrations.AddField(
            model_name='journal',
            name='volume',
            field=models.CharField(max_length=10, verbose_name='volume', blank=True),
        ),
        migrations.AddField(
            model_name='photo',
            name='format',
            field=models.CharField(max_length=50, verbose_name='format', blank=True),
        ),
        migrations.AddField(
            model_name='photo',
            name='subject',
            field=models.CharField(max_length=191, verbose_name='sujet photographi\xe9', blank=True),
        ),
        migrations.AddField(
            model_name='posterbooklet',
            name='format',
            field=models.CharField(max_length=50, verbose_name='format', blank=True),
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
            name='EditedDocument',
        ),
        migrations.AddField(
            model_name='bookthesis',
            name='edition_place',
            field=models.ForeignKey(verbose_name='edition place', blank=True, to='mcm.EditionPlace', null=True),
        ),
        migrations.AddField(
            model_name='disc',
            name='captation',
            field=models.ForeignKey(verbose_name='captation', blank=True, to='mcm.Captation', null=True),
        ),
        migrations.AddField(
            model_name='journal',
            name='classification',
            field=models.ForeignKey(verbose_name='thematic classification', blank=True, to='mcm.Classification', null=True),
        ),
        migrations.AddField(
            model_name='photo',
            name='captation',
            field=models.ForeignKey(verbose_name='captation', blank=True, to='mcm.Captation', null=True),
        ),
        migrations.AddField(
            model_name='video',
            name='captation',
            field=models.ForeignKey(verbose_name='captation', blank=True, to='mcm.Captation', null=True),
        ),
        migrations.AddField(
            model_name='videofile',
            name='captation',
            field=models.ForeignKey(verbose_name='captation', blank=True, to='mcm.Captation', null=True),
        ),
    ]

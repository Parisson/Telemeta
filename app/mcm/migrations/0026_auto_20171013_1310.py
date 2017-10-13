# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mcm', '0025_auto_20170922_1600'),
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
        migrations.CreateModel(
            name='Illustration',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=191, verbose_name='name')),
            ],
            options={
                'verbose_name': 'illustration',
            },
        ),
        migrations.CreateModel(
            name='isEdited',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('collection_num', models.CharField(max_length=50, verbose_name='collection number', blank=True)),
                ('companion', models.CharField(max_length=50, verbose_name="mat\xe9riel d'accompagnement", blank=True)),
                ('collection', models.ForeignKey(verbose_name='collection', blank=True, to='mcm.Collection', null=True)),
                ('language', models.ManyToManyField(to='mcm.Language', verbose_name='language')),
            ],
        ),
        migrations.CreateModel(
            name='Support',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=191, verbose_name='name')),
            ],
            options={
                'verbose_name': 'Support',
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
            name='color',
            field=models.CharField(blank=True, max_length=2, verbose_name='color', choices=[('C', 'Couleur'), ('NB', 'Noir et Blanc')]),
        ),
        migrations.AddField(
            model_name='bookthesis',
            name='format',
            field=models.CharField(max_length=50, verbose_name='format', blank=True),
        ),
        migrations.AddField(
            model_name='disc',
            name='duration',
            field=models.CharField(max_length=50, verbose_name='duration', blank=True),
        ),
        migrations.AddField(
            model_name='document',
            name='contient_contenu_dans',
            field=models.ManyToManyField(related_name='_document_contient_contenu_dans_+', verbose_name='Contient ou contenu dans', to='mcm.Document'),
        ),
        migrations.AddField(
            model_name='document',
            name='page_num',
            field=models.CharField(max_length=50, verbose_name='number of pages', blank=True),
        ),
        migrations.AddField(
            model_name='document',
            name='parents',
            field=models.ManyToManyField(related_name='_document_parents_+', verbose_name='Contient ou contenu dans', to='mcm.Document'),
        ),
        migrations.AddField(
            model_name='journal',
            name='format',
            field=models.CharField(max_length=50, verbose_name='format', blank=True),
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
            name='color',
            field=models.CharField(blank=True, max_length=2, verbose_name='color', choices=[('C', 'Couleur'), ('NB', 'Noir et Blanc')]),
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
            name='color',
            field=models.CharField(blank=True, max_length=2, verbose_name='color', choices=[('C', 'Couleur'), ('NB', 'Noir et Blanc')]),
        ),
        migrations.AddField(
            model_name='posterbooklet',
            name='format',
            field=models.CharField(max_length=50, verbose_name='format', blank=True),
        ),
        migrations.AddField(
            model_name='video',
            name='color',
            field=models.CharField(blank=True, max_length=2, verbose_name='color', choices=[('C', 'Couleur'), ('NB', 'Noir et Blanc')]),
        ),
        migrations.AddField(
            model_name='video',
            name='duration',
            field=models.CharField(max_length=50, verbose_name='duration', blank=True),
        ),
        migrations.AddField(
            model_name='videofile',
            name='color',
            field=models.CharField(blank=True, max_length=2, verbose_name='color', choices=[('C', 'Couleur'), ('NB', 'Noir et Blanc')]),
        ),
        migrations.AddField(
            model_name='videofile',
            name='duration',
            field=models.CharField(max_length=50, verbose_name='duration', blank=True),
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
            model_name='bookthesis',
            name='illustration',
            field=models.ForeignKey(verbose_name='illustration', blank=True, to='mcm.Illustration', null=True),
        ),
        migrations.AddField(
            model_name='disc',
            name='captation',
            field=models.ForeignKey(verbose_name='captation', blank=True, to='mcm.Captation', null=True),
        ),
        migrations.AddField(
            model_name='disc',
            name='support',
            field=models.ForeignKey(verbose_name='support', blank=True, to='mcm.Support', null=True),
        ),
        migrations.AddField(
            model_name='journal',
            name='classification',
            field=models.ForeignKey(verbose_name='thematic classification', blank=True, to='mcm.Classification', null=True),
        ),
        migrations.AddField(
            model_name='journal',
            name='illustration',
            field=models.ForeignKey(verbose_name='illustration', blank=True, to='mcm.Illustration', null=True),
        ),
        migrations.AddField(
            model_name='photo',
            name='captation',
            field=models.ForeignKey(verbose_name='captation', blank=True, to='mcm.Captation', null=True),
        ),
        migrations.AddField(
            model_name='photo',
            name='support',
            field=models.ForeignKey(verbose_name='support', blank=True, to='mcm.Support', null=True),
        ),
        migrations.AddField(
            model_name='posterbooklet',
            name='illustration',
            field=models.ForeignKey(verbose_name='illustration', blank=True, to='mcm.Illustration', null=True),
        ),
        migrations.AddField(
            model_name='video',
            name='captation',
            field=models.ForeignKey(verbose_name='captation', blank=True, to='mcm.Captation', null=True),
        ),
        migrations.AddField(
            model_name='video',
            name='support',
            field=models.ForeignKey(verbose_name='support', blank=True, to='mcm.Support', null=True),
        ),
        migrations.AddField(
            model_name='videofile',
            name='captation',
            field=models.ForeignKey(verbose_name='captation', blank=True, to='mcm.Captation', null=True),
        ),
        migrations.AddField(
            model_name='videofile',
            name='support',
            field=models.ForeignKey(verbose_name='support', blank=True, to='mcm.Support', null=True),
        ),
    ]

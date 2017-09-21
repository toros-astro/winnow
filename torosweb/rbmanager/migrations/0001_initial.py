# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('winnow', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Experiment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField(verbose_name=b'date of experiment')),
                ('platform', models.CharField(default=b'0', max_length=1, verbose_name=b'software used', choices=[(b'0', b'Weka'), (b'1', b'RapidMiner'), (b'2', b'scikit-learn'), (b'3', b'Other')])),
                ('other_platform_name', models.CharField(max_length=20, null=True, blank=True)),
                ('alg_name', models.CharField(max_length=50, verbose_name=b'algorithm name')),
                ('params_file', models.FileField(max_length=50, upload_to=b'', null=True, verbose_name=b'parameter file name', blank=True)),
                ('labels_file', models.FileField(upload_to=b'', null=True, verbose_name=b'label file name', blank=True)),
                ('featureset_infofile', models.FileField(upload_to=b'', null=True, verbose_name=b'feature set file name', blank=True)),
                ('featuretable_datafile', models.FileField(upload_to=b'', null=True, verbose_name=b'feature table file name', blank=True)),
                ('conf_mat_rr', models.IntegerField(verbose_name=b'reals classified as reals')),
                ('conf_mat_rb', models.IntegerField(verbose_name=b'reals classified as bogus')),
                ('conf_mat_br', models.IntegerField(verbose_name=b'bogus classified as reals')),
                ('conf_mat_bb', models.IntegerField(verbose_name=b'bogus classified as bogus')),
                ('confusion_table_file', models.FileField(upload_to=b'', null=True, verbose_name=b'confusion matrix file name', blank=True)),
                ('other_outputfiles', models.TextField(null=True, verbose_name=b'other output files', blank=True)),
                ('other_inputfiles', models.TextField(null=True, verbose_name=b'other input files', blank=True)),
                ('description', models.TextField(null=True, blank=True)),
                ('dataset', models.ForeignKey(to='winnow.Dataset')),
                ('user', models.ForeignKey(to='winnow.UserProfile')),
            ],
        ),
    ]

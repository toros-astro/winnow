# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Alert',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ligo_run', models.CharField(max_length=20, verbose_name=b'LIGO run')),
                ('alert_number', models.IntegerField()),
                ('datetime', models.DateTimeField()),
                ('description', models.TextField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime', models.DateTimeField()),
                ('is_taken', models.BooleanField(default=False)),
                ('was_observed', models.BooleanField(default=False)),
                ('alert', models.ForeignKey(to='broker.Alert')),
            ],
        ),
        migrations.CreateModel(
            name='GWGCCatalog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('pgc', models.IntegerField(verbose_name=b'PGC Identifier from HYPERLEDA')),
                ('name', models.CharField(max_length=20, verbose_name=b'Common Name')),
                ('ra', models.FloatField(null=True, verbose_name=b'Right Ascension', blank=True)),
                ('dec', models.FloatField(null=True, verbose_name=b'Declination', blank=True)),
                ('obj_type', models.FloatField(null=True, verbose_name=b'Type', blank=True)),
                ('app_mag', models.FloatField(null=True, verbose_name=b'Apparent Blue Magnitude', blank=True)),
                ('maj_diam_a', models.FloatField(null=True, verbose_name=b'Major Diameter(a)', blank=True)),
                ('err_maj_diam', models.FloatField(null=True, verbose_name=b'Error in Major Diameter', blank=True)),
                ('min_diam_b', models.FloatField(null=True, verbose_name=b'Minor diameter (b) ', blank=True)),
                ('err_min_diam', models.FloatField(null=True, verbose_name=b'Error in Minor diameter', blank=True)),
                ('b_over_a', models.FloatField(null=True, verbose_name=b'b/a(Ratio of minor to major diameters) ', blank=True)),
                ('err_b_over_a', models.FloatField(null=True, verbose_name=b'Error b/a (Ratio of minor to major diameters)', blank=True)),
                ('pa', models.FloatField(null=True, verbose_name=b'Position Angle of Galaxy', blank=True)),
                ('abs_mag', models.FloatField(null=True, verbose_name=b'Absolute Blue Magnitude', blank=True)),
                ('dist', models.FloatField(null=True, verbose_name=b'Distance', blank=True)),
                ('err_dist', models.FloatField(null=True, verbose_name=b'Error on Distance', blank=True)),
                ('err_app_mag', models.FloatField(null=True, verbose_name=b'Error on Apparent blue magnitude', blank=True)),
                ('err_abs_mag', models.FloatField(null=True, verbose_name=b'Error on Absolute blue magnitude', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Observatory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('short_name', models.CharField(max_length=10, null=True, blank=True)),
                ('country', models.CharField(max_length=20)),
                ('city', models.CharField(max_length=20)),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('elevation', models.FloatField()),
            ],
            options={
                'verbose_name_plural': 'observatories',
            },
        ),
        migrations.AddField(
            model_name='assignment',
            name='observatory',
            field=models.ForeignKey(to='broker.Observatory'),
        ),
        migrations.AddField(
            model_name='assignment',
            name='target',
            field=models.ForeignKey(to='broker.GWGCCatalog'),
        ),
    ]

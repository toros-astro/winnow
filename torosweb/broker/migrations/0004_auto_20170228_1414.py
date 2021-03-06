# -*- coding: utf-8 -*-
# Generated by Django 1.9.12 on 2017-02-28 20:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('broker', '0003_auto_20160924_1736'),
    ]

    operations = [
        migrations.AddField(
            model_name='alert',
            name='grace_id',
            field=models.CharField(default='Unknown', max_length=20, verbose_name=b'GraceDB ID'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='alert',
            name='alert_number',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='alert',
            name='ligo_run',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name=b'LIGO run'),
        ),
    ]

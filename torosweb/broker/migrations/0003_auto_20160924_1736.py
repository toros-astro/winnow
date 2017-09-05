# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('broker', '0002_assignment_probability'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gwgccatalog',
            name='obj_type',
            field=models.CharField(max_length=5, null=True, verbose_name=b'Type', blank=True),
        ),
    ]

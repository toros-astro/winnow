# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('broker', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignment',
            name='probability',
            field=models.FloatField(default=0.0, null=True, blank=True),
        ),
    ]

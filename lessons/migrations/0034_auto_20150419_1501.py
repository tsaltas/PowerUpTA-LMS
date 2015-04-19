# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0033_auto_20150419_1459'),
    ]

    operations = [
        migrations.AlterField(
            model_name='step',
            name='step_activity',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
    ]

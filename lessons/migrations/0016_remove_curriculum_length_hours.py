# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0015_auto_20150218_1745'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='curriculum',
            name='length_hours',
        ),
    ]

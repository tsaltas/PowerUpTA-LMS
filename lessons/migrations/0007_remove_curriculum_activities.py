# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0006_auto_20150129_1650'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='curriculum',
            name='activities',
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0002_auto_20150129_1500'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='activity',
            options={'verbose_name_plural': 'activities'},
        ),
        migrations.AlterModelOptions(
            name='activityrelationship',
            options={'verbose_name': 'relationship', 'verbose_name_plural': 'relationships'},
        ),
        migrations.AlterModelOptions(
            name='curriculum',
            options={'verbose_name_plural': 'curricula'},
        ),
    ]

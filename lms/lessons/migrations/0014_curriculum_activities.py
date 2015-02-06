# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0013_auto_20150129_1842'),
    ]

    operations = [
        migrations.AddField(
            model_name='curriculum',
            name='activities',
            field=models.ManyToManyField(to='lessons.Activity', through='lessons.CurriculumActivityRelationship'),
            preserve_default=True,
        ),
    ]

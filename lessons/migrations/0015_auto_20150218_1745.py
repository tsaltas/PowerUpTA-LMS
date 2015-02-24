# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0014_curriculum_activities'),
    ]

    operations = [
        migrations.AlterField(
            model_name='curriculum',
            name='activities',
            field=models.ManyToManyField(to='lessons.Activity', through='lessons.CurriculumActivityRelationship', blank=True),
            preserve_default=True,
        ),
    ]

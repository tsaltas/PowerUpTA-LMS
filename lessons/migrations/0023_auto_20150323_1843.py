# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0022_auto_20150322_1923'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activityrelationship',
            name='rel_type',
            field=models.CharField(max_length=3, verbose_name=b'Relationship Type', choices=[(b'sub-activity', b'sub-activity'), (b'super-activity', b'super-activity'), (b'extension', b'extension')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='curriculum',
            name='activities',
            field=models.ManyToManyField(related_name='curricula', through='lessons.CurriculumActivityRelationship', to='lessons.Activity', blank=True),
            preserve_default=True,
        ),
    ]

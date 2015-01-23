# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0002_auto_20150121_2131'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lesson',
            name='curriculum',
        ),
        migrations.AddField(
            model_name='curriculum',
            name='lessons',
            field=models.ManyToManyField(to='lessons.Lesson'),
            preserve_default=True,
        ),
    ]

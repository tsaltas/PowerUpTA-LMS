# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='curriculum',
            name='lessons',
        ),
        migrations.AddField(
            model_name='lesson',
            name='curriculum',
            field=models.ManyToManyField(to='lessons.Curriculum'),
            preserve_default=True,
        ),
    ]

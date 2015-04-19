# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0032_auto_20150419_1450'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='activity',
            name='steps',
        ),
        migrations.AddField(
            model_name='step',
            name='activity',
            field=models.ForeignKey(default=1, to='lessons.Activity'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='step',
            name='step_activity',
            field=models.IntegerField(blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='step',
            name='text',
            field=models.CharField(max_length=50),
            preserve_default=True,
        ),
    ]

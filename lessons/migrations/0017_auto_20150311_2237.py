# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0016_remove_curriculum_length_hours'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='materials',
            field=models.ManyToManyField(related_name='activities', to='lessons.Material', blank=True),
            preserve_default=True,
        ),
    ]

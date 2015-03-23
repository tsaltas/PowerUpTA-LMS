# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0021_auto_20150317_2108'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='tags',
            field=models.ManyToManyField(related_name='activities', to='lessons.Tag'),
            preserve_default=True,
        ),
    ]

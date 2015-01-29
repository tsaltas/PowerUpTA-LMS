# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='video',
            field=models.URLField(blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='material',
            name='url',
            field=models.URLField(),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='resource',
            name='url',
            field=models.URLField(),
            preserve_default=True,
        ),
    ]
